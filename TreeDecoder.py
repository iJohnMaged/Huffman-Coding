# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 18:17:08 2017

@author: LegendJo
"""

from BinTree import Node

def generateTree(msg):
    b = None
    if(len(msg) > 0):
        b = msg.pop(0)
    return readTree(b, msg)

def nextBit(msg):
    if len(msg) > 0:
        return msg.pop(0)
    else:
        return None

def readTree(b, msg):
    if b == None:
        return None
    # print("chr b", chr(b))
    if (chr(b) == "0"):
        c = nextBit(msg)
        root = Node(c, 0)
    elif (chr(b) == "1"):
        root = Node(0, 0, readTree(nextBit(msg), msg), readTree(nextBit(msg), msg))
    return root
