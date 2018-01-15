from HuffmanTree import HuffmanTree
import fileIO, time
import sys

class HuffmanCompressor(object):

    def __init__(self, dest):
        self.dest = dest

    def getCodedFile(self, text, codes):

        """Generates the coded-version of the original content
        which consists of bits of 0s and 1s representing huffman-codings.

        No delimiters is required between codes because in huffman-codings by
        definition a code of a character can never be the start of another's code.

        Args:
            text (str): The original content of the file.
            codes (dict): representing huffman codings
        Returns:
            codedFile (str): The coded representation of the original file.
        """

        # Generates the codes required to encode the original file.

        codedfile_list = [codes[ch] for ch in text]
        codedFile = ''.join(codedfile_list)

        return codedFile

    def convertToByteArr(self, codedtext, codedTree, target):

        """Final stage of generating the encoded file.
        This method formats the encoded file-header first as follows:
        *1st bit: Information about extra bits added to the file.
                - Huffman-codings often doesn't turn out as exact multiple
                - of 8s so we add trailing "0"s to the coded text.
        *2nd - 5th bits: Contains the size of the representation of huffman-tree.
                - We need to add the huffman-tree representation to the file-header
                - So we can decompress the files later.
                - In big files, the overhead can be negligible.
        *6th-nth bits: representation of huffman-tree.
                - n is determined by bits 2nd-5th.

        Args:
            codedtext (str): binary representation of the original file.

        Return:
            byteArr (bytearray): Bytes sequence of the final content to be written to a file.
        """

        # adding extra bits to make the codedtext a multiple of 8
        # storing the extra bits information in first bit

        bits = 8 - len(codedtext) % 8
        if bits != 0:
            codedtext += ("0" * bits)

        byteArr = bytearray()
        byteArr.append(bits)
        # representation of huffman-tree to be stored in file header.
        # length is stored in bits 2-5

        ln = len(codedTree)
        ba = ln.to_bytes(4, byteorder="little")

        byteArr.extend(ba)
        byteArr.extend(codedTree)

        # Encode the original file name and relative path

        extlnBa = len(target).to_bytes(4, byteorder="little")
        byteArr.extend(extlnBa)
        for ch in target:
            byteArr.append(ord(ch))

        textBa = bytearray()
        # store each 8 binary sequence as a byte so we can actually save space

        #This is way faster than the code commented below!
        textBa.extend(int(codedtext,2).to_bytes((len(codedtext))//8, byteorder="big"))

        # for i in range(0, len(codedtext), 8):
        #     b = codedtext[i:i + 8]
        #     textBa.append(int(b, 2))

        byteArr.extend(len(textBa).to_bytes(4, byteorder="little"))
        byteArr.extend(textBa)


        fileSize = len(byteArr)
        fzByte = fileSize.to_bytes(4, "little")
        byteArr = fzByte + byteArr

        return byteArr

    def compress(self, src, target):

        """After initializing huffman Object, a call to this method
        will compress the file pointed to by the member variable path.

        Write bytes object to the target file.
        Returns:
            tuple (double, double): Contains information about comprission ratios
        """

        t1 = time.time()
        with open(src, "rb") as f:
            # Read text from file
            text = f.read()

        if len(text) == 0:
            raise EOFError("Empty file")

        # Calculate frequency and build Huffman Tree
        tree = HuffmanTree()
        codes = tree.initializeTree(text)

        # print("dictionary size: ", sys.getsizeof(codes))
        # Code the text and convert it into an array of bytes and write it to file
        codedText = self.getCodedFile(text, codes)
        codedTree = tree.encodeTree()

        # print("tree size: ", sys.getsizeof(codedTree))
        #
        # print("Saved tree to file:", codedTree.decode("utf-8"))
        byteArr = self.convertToByteArr(codedText, codedTree,target)

        with open(self.dest, "ab") as f2:
            f2.write(bytes(byteArr))

        t2 = time.time()
        self.outputCodes(codes, fileIO.fileName(src))

        t = t2-t1
        return t

    def outputCodes(self, codes, target):
        """auxiliary method to output the huffman-codings to a file.
        Returns:
            None.
        """

        offset = 20
        fileIO.create_path_nexist("codes/")

        target = "codes/" + fileIO.alterExten(fileIO.addToName(target, "codes"), "txt")

        with open(target, "w") as f:
            header = "BYTE" + " " * (offset - 4) + "CODE" + " " * (offset - 4) + "New Code\n"
            f.write(header)

            for code in codes:
                sCode = str(code)
                bCode = format(code, '08b')
                row = sCode + " " * (offset - len(sCode)) + bCode + " " * (offset - len(bCode)) + codes[
                    code] + "\n"
                f.write(row)
