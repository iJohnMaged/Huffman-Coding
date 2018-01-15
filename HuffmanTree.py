from BinTree import Node
from heapq import heappop, heappush, heapify
from collections import Counter

class HuffmanTree(object):

    def __init__(self, root=None):
        self.heap = []
        self.root = root

    def calculateFrequency(self, text):

        """Calculates how many times a character appears in text

        ARGS:
            text (str): text to be calculated

        Returns:
            Counter Object - dict (int, int): Maps int value of a character to how many times it appeared in text

        Example:
            "ABCDDAAaaBZ" should return Counter({'A': 3, 'B': 2, 'C': 1, 'D': 2, 'a': 2, 'Z': 1})
        """

        # Efficient counting
        result = Counter(text)

        return result

    def buildMinHeap(self, freq):

        """Builds a minimum heap tree of Node objects, sorted by
        the frequency of each Node.

        Args:
            freq dict(int, int): Mapping of int value of a character to its frequency

        Returns:
            None
        """

        # For each character present in the original file, create a Node and add it the tree

        self.heap = [Node(char,frequency) for char,frequency in freq.items()]

        heapify(self.heap)

    def makeTreeFromHeap(self):

        """Builds the actual huffman-tree.

        ALGORITHM:
            While heap has more than 1 Node:
                * Deque the two lowest frequencies Nodes.
                * Create a new Internal-Node, With a frequency equal to the sum of two.
                * Queue the new Internal-Node
        RETURNS:
            None
        """

        while (len(self.heap) > 1):
            node1 = heappop(self.heap)
            node2 = heappop(self.heap)

            freq = int(node1.freq) + int(node2.freq)

            heappush(self.heap, Node(0, freq, node1, node2))

        self.root = heappop(self.heap)


    def generateCodes(self, root=False,codes = None, prevCode=""):

        """Generates Huffman-Codes by traversing the Huffman-tree recursively.
        Starting form the root of tree, left branch represents a bit value of "0"
        and right branch represents a bit value of "1".

        Example:
                         *
                       0/ 1\
                     0/\1   0/\1
                    0/\1 c  d  e
                   a  b
        Codes generated are : {'a': 000, 'b': 001, 'c': 01, 'd': 10, 'e': 11}

        Args:
            root (Node): root of the huffman-tree
            prevCode (str): Not-required by the caller of the function at all,
                            Unless a prefix to codes is required.
        """

        if codes is None:
            codes = {}

        if root is False:
            root = self.root

        if root is None:
            return

        r = root.right
        l = root.left

        # if left Node doesn't exist then we're at a leaf-node.
        if not l:
            # Checks if the root is the only element in the Huffman-Tree
            if prevCode == "": prevCode = "0"
            codes[root.val] = prevCode

        self.generateCodes(l,codes, prevCode + "0")
        self.generateCodes(r,codes, prevCode + "1")

        return codes

    def initializeTree(self, text):

        freq = self.calculateFrequency(text)
        self.buildMinHeap(freq)
        self.makeTreeFromHeap()

        return self.generateCodes()

    def encodeTree(self, root=False, ba = None):
        """Recursively generates a representation of huffman-tree
        to be stored in file-header

        Args:
            root (Node): a Node-object representing a single node in the huffman Tree
                        It's the root of the tree by default.
        Returns:
            None
        """

        if root is False:
            root = self.root

        if ba is None:
            ba = bytearray()

        # At leaf node, represent it with a 0 followed by
        # the value at that node.
        # At internal-node, represent it with 1 and traverse left, right.

        if not root.left:
            ba.append(ord("0"))
            ba.append(root.val)
        else:
            ba.append(ord("1"))
            self.encodeTree(root.left, ba)
            self.encodeTree(root.right, ba)

        return ba
