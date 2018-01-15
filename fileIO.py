# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 19:43:05 2017

@author: LegendJo
"""

import errno
import os

def splitext_(path):
    fileName, ext = os.path.splitext(path)
    return [fileName, ext[1:]]

def basename(path):
    return splitext_(os.path.basename(path))[0]

def fileName(path):
    return os.path.basename(path)

def fileExtension(path):
    return os.path.splitext(path)[1][1:]

def addToName(path, word):
    fileName, ext = os.path.splitext(path)
    return fileName + word + ext

def alterExten(path, newExten):
    fileName, ext = os.path.splitext(path)
    return fileName + "." + newExten

def dirname_(path):
    return os.path.split(os.path.abspath(path))[0]

def size(path):
    return os.path.getsize(path)

def dir_size(path):
    total_size = 0
    for p, dirs, files in os.walk(path):
        for f in files:
            total_size += size(os.path.join(p,f))
    return total_size

def outputFile(p):
    p = os.path.join(p, '')
    return os.path.join(os.getcwd(), '') + os.path.basename(os.path.dirname(p)) + ".huffman"

def huffman_file_path(p, dir=False):

    if not dir:
        return os.path.join(os.getcwd(), '') + alterExten(p, "huffman")

    return outputFile(p)


def files_to_process(p):

    if os.path.isdir(p):
        files, original_size = listFiles(p)
        output = huffman_file_path(p, True)

    elif os.path.isfile(p):
        files = {os.path.basename(p): p}
        original_size = size(p)
        output = huffman_file_path(p)

    else:
        raise FileNotFoundError

    return files, original_size, output

def listFiles(path):

    f = {}
    total_size = 0
    path = path.rstrip(os.sep)
    parent = os.path.dirname(path)

    for p, dirs, files in os.walk(path):
        for file in files:
            fp = os.path.join(p,file)
            total_size += size(fp)
            f[(os.path.relpath(os.path.join(p,file), parent))] = fp

    return (f, total_size)

def create_path_nexist(path):

    dr = os.path.dirname(path)
    if not dr:
        return
    try:
        os.makedirs(dr)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def invert_dict(d):
    return dict([(v, k) for k, v in d.items()])
