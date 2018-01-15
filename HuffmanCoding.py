# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 04:35:47 2017

Alexandria University - Engineering College.
SSP - CCE Department

@author: John Maged Adly
@id: 3690

"""

from HuffmanCompressor import HuffmanCompressor
from HuffmanDecomporessor import HuffmanDecompressor

class Huffman(object):

    def __init__(self, files, huffman_file):

        """
        Args:
            files dict(str, str): Dictionary mapping path of a file to it's full path.
            huffman_file str: path/file to be compressed OR file to be decompressed.
        """

        self.files = files
        self.huffman_file = huffman_file

    def compress(self):

        exec_time = 0
        compressor = HuffmanCompressor(self.huffman_file)

        # To override the file if it exists
        open(self.huffman_file, "w").close()

        with open(self.huffman_file, "ab") as f:
            ba = len(self.files).to_bytes(4, byteorder="little")
            f.write(ba)

        for path, file_ in self.files.items():
            exec_time += compressor.compress(file_, path)

        return exec_time

    def decompress(self):
        
        decompressor = HuffmanDecompressor(self.huffman_file)
        return decompressor.decomp()
