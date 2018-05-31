#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import bottleneck as bn
from gnuradio import gr

class decide_threshold(gr.sync_block):
    """
    docstring for block decide_threshold
    """
    __shared_state = {}

    def __init__(self, window_size = None):
        self.__dict__ = self.__shared_state
        if len(self.__dict__) != 0:
            return

        gr.sync_block.__init__(self,
            name = "decide_threshold",
            in_sig = [np.float32],
            out_sig = [np.float32],
        )

        self.data = np.empty(0)
        self.threshold = None
        self.window_size = window_size
        self.history = np.empty(0)


    def work(self, input_items, output_items):
        self.update(input_items[0])

        output_items[0][:] = input_items[0]
        return len(output_items[0])


    def get_threshold(self):
        return self.threshold


    def get_threshold_average(self):
        return np.average(self.history) / 2


    def set_threshold(threshold):
        self.threshold = threshold


    def update(self, arr):
        self.data = np.append(self.data, arr[:self.window_size])

        if len(self.data) > self.window_size:
            arr_pre = self.data[:self.window_size]
            self.data = arr[-(self.window_size-1):]

            top10_arr = -bn.partition(-arr_pre, 10)[:10]
            self.threshold = np.average(top10_arr) / 2.6
            self.history = np.append(self.history, self.threshold)
            if len(self.history) > 10:
                self.history = self.history[1:]
