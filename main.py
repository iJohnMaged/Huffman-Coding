# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 17:53:32 2017

@author: LegendJo
"""

from HuffmanCoding import Huffman
import os, argparse, fileIO, time


parser = argparse.ArgumentParser(description='Huffman Compressing and Decompressing.')

parser.add_argument('path', type=str, help="Path and name of file to compress / decompress")
parser.add_argument('-m', '--method', choices=["compress", "decompress"], default="compress",required=True, help="Chooses whether to compress or decompress file")

args = parser.parse_args()

p = args.path

files, original_size, huffman_file = fileIO.files_to_process(p)
huffman = Huffman(files, huffman_file)

if args.method == "compress":

    exec_time = huffman.compress()
    output_size = fileIO.size(huffman_file)
    compression_ratio = original_size / output_size
    space_saved = (1 - 1/compression_ratio)

    print("**************************************")
    print("* Compressing finished in %.2f seconds" % exec_time)
    print("* Compression Ratio %.2f" % compression_ratio)
    print("* Space Saved: {0:.2%}".format(space_saved) )
    print("**************************************")

if args.method == "decompress":

    if fileIO.fileExtension(p).lower() != "huffman":
        print("Invalid file format, *.huffman file needed")
        exit(1)

    exec_time = huffman.decompress()

    print("****************************************")
    print("* Decompressing finished in %.2f seconds" % exec_time)
    print("****************************************")
