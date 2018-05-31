#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from gnuradio import gr

class differential(gr.sync_block):
    """
    docstring for block differential
    """
    def __init__(self, h):
        gr.sync_block.__init__(self,
            name="differential",
            in_sig = [np.float32],
            out_sig = [np.float32],
        )

        self.h = h
        self.prev = np.array([0])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        in0 = np.append(self.prev, in0)
        out[:] = np.diff(in0) / self.h
        self.prev = np.array([in0[-1]])

        return len(output_items[0])
