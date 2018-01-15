# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 19:45:43 2017

@author: LegendJo
"""

class Node(object):

    def __init__(self, val, freq, left = None, right = None):
        self.left = left
        self.right = right
        self.val = val
        self.freq = freq

    def __lt__(self, other):
        return self.freq < other.freq

    def __str__(self):
        return "Value: " + str(self.val) + " Freq: " + str(self.freq)

    def __repr__(self):
        return self.__str__()
