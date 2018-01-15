from TreeDecoder import generateTree
from HuffmanTree import HuffmanTree

import os, tempfile
import fileIO
import time

class HuffmanDecompressor(object):

    def __init__(self, src):
        self.src = src

    def getDecodedFile(self, text, tree):

        """Decodes the compressed file content to original file's content by
        grouping "0"s and "1"s in the binary sequence until it matches a huffman-code.

        Args:
            text (str): Binary sequence to be decoded.
            tree (HuffmanTree object).

        Returns:
            bytearray object - bytes of the original file.
        """

        original_file = bytearray()
        root = tree.root
        # decision = {'0': lambda root: root.left, '1': lambda root: root.right}

        for ch in text:
            # root = decision[ch](root)
            if ch == "0":
                root = root.left
            else:
                root = root.right
            if root.left is None:
                original_file.append(root.val)
                root = tree.root

        return original_file


    def decomp(self):

        """Auxiliary method to loop through all compressed files
            and decompress each one at a time
        """

        with open(self.src, "rb") as f:
            fd = f.fileno()
            number_of_files = int.from_bytes(os.read(fd, 4), "little")

            t1 = time.time()
            for i in range(number_of_files):
                fileSize = int.from_bytes(os.read(fd, 4), "little")

                file = os.read(fd, fileSize)

                if not file:
                    break
                f2 = tempfile.TemporaryFile(mode="wb")
                f2.write(file)
                f2.seek(0)
                self.decompress(f2)
                f2.close()
            t2 = time.time()

        return t2-t1



    def decompress(self, f):

        """After initializing huffman Object, a call to this method
        will read information from the file-header and decode the file accordingly.

        Write bytes object to the target file.

        Args:
            f (TemporaryFile): file to be compressed
        Returns:
            None
        """

        fd = f.fileno()

        ############################
        # READING HEADER INFORMATION
        ############################

        # Get number of extra bits that was added to last byte
        byte = os.read(fd, 1)
        bits = ord(byte)

        # Get the size of encoded Huffman-Tree, read it from header and reconstruct it
        byte = os.read(fd, 4)

        length = int.from_bytes(byte, byteorder="little")
        byte = os.read(fd, length)

        root = generateTree(bytearray(byte))
        tree = HuffmanTree(root=root)

        # Get the original file name and path (in case of folder compression)
        byte = os.read(fd, 4)

        ln = int.from_bytes(byte, byteorder="little")
        target = ""

        for i in range(ln):
            byte = os.read(fd, 1)
            target += byte.decode("utf-8")


        fileContent = os.read(fd, 4)

        fileContentLn = int.from_bytes(fileContent, "little")

        # read the rest of the file byte by byte
        # convert it to binary representation
        # to be decoded

        byte = os.read(fd, fileContentLn)
        hexa = byte.hex()
        bitsNo = "0" + str(fileContentLn*8)
        formattedOutput = '{0:' + bitsNo + 'b}'
        output_bin = formattedOutput.format(int(hexa, 16))

        # Delete the extra bits
        if bits != 0:
            output_bin = output_bin[: -1 * bits]


        output = self.getDecodedFile(output_bin, tree)
        fileIO.create_path_nexist(target)

        with open(target, "wb") as f2:
            f2.write(output)
