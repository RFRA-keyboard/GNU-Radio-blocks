#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from gnuradio import gr
from decide_threshold import decide_threshold

class detect_preamble(gr.sync_block):
    """
    docstring for block detect_preamble
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="detect_preamble",
            in_sig = [np.float32],
            out_sig = [np.float32],
        )

        self.samp_per_bit = 6.7
        self.half_samp_per_bit = int(np.floor_divide(self.samp_per_bit, 2))


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        self.window = in0

        th = decide_threshold().get_threshold()

        if th:
            count = 0
            upper = in0 > th
            lower = in0 < -th

            over = np.logical_or(upper, lower)

            indexes = np.where(over == True)[0]

            if len(indexes) > 0:
                index = indexes[0]
                if (index + 100) < len(in0):
                    sign = 1 if in0[index] > 0 else  -1
                    self.detect(index, sign)

        out[:] = in0
        return len(output_items[0])


    def detect(self, index, sign):
        found = self.find_next_six(index, sign)

        if found is None:
            return

        coefficient = found[0]
        next_start_point = found[1]
        next_count = found[2]

        if next_count != 6:
            return

        changes = np.array([sign])
        changes = np.append(changes, self.decode(index, next_count, sign))

        binary = self.decode_nrzi(changes)
        if len(binary) > 6:
            if binary[0:7] == [0, 0, 0, 0, 0, 0, 0]:
                print sign, ''.join(map(str, binary)), '%05.10f' % decide_threshold().get_threshold_average()

    def decode(self, start, division, sign):
        decoded = np.empty(0)
        sign *= -1
        for i in range(1, division + 1, 1):
            point = start + np.round(self.samp_per_bit * i)
            found = self.find_maximum_point(point, sign)
            coefficient = found[0]
            max_point = found[1]
            if coefficient != 0:
                sign *= -1

            decoded = np.append(decoded, coefficient)
        return decoded


    def find_next_seven(self, index):
        for i in range(7, 0, -1):
            estimated = np.round(self.samp_per_bit * i)
            found = self.find_maximum_point(index + estimated)
            coefficient = found[0]
            max_point = found[1]

            if np.absolute(coefficient) > 0:
                return [coefficient, max_point, i]

        return None


    def find_next_six(self, index, sign):
        estimated = np.round(self.samp_per_bit * 6)
        found = self.find_maximum_point(index + estimated, sign)
        coefficient = found[0]
        max_point = found[1]

        if np.absolute(coefficient) > 0:
            return [coefficient, max_point, 6]
        else:
            return None


    def find_maximum_point(self, index, sign = 0):
        if sign == 0:
            return
        index = int(index)

        left = index - self.half_samp_per_bit
        right = index + self.half_samp_per_bit
        min_or_max_point = 0

        if sign > 0:
            min_or_max_point = np.argmax(self.window[left:right]) + index - self.half_samp_per_bit
        else:
            min_or_max_point = np.argmin(self.window[left:right]) + index - self.half_samp_per_bit

        return [self.coefficient_of(self.window[min_or_max_point]), min_or_max_point]


    def compare(self, left, right, which):
        left = int(left)
        right = int(right)
        if which == 'max':
            if self.window[left] > self.window[right]:
                bigger = self.window[left]
                bigger_point = left
            else:
                bigger = self.window[right]
                bigger_point = right
            return [bigger, bigger_point]
        else:
            if self.window[left] < self.window[right]:
                smaller = self.window[left]
                smaller_point = left
            else:
                smaller = self.window[right]
                smaller_point = right
            return [smaller, smaller_point]


    def update(self, current, max, current_point, max_point, sign):
        if (current * sign) > (max * sign):
            return [current, current_point]
        else:
            return [max, max_point]

    def coefficient_of(self, value):
        if np.absolute(value) < decide_threshold().get_threshold():
            return 0
        else:
            if value > 0:
                return 1
            else:
                return -1


    def decode_nrzi(self, nrzi):
        binary = []

        for change in nrzi:
            if change == 0:
                binary.append(1)
            else:
                binary.append(0)

        return binary
