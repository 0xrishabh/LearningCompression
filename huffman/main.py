from bitarray import bitarray
from queue import PriorityQueue
import sys

class Node:
    def __init__(self, symbol, value):
        self.value = value
        self.symbol = symbol
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.value < other.value
    

class HuffMan:
    def __init__(self, text):
        # Storage
        self.text = text
        self.root = None
        self.freq = {}
        self.encodeTable = {}
        self.decodeTable = {}
        # Execution
        self._buildFreq(text)
        queue = self._buildQueue()
        self._buildTree(queue)
        self._buildTables(self.root)

    def _buildFreq(self, text):
        for char in text:
            self.freq[char] = self.freq.get(char, 0) + 1
    
    def _buildQueue(self):
        queue = PriorityQueue()
        for char,freq in self.freq.items():
            node = Node(char, freq)
            queue.put(node)
        return queue

    def _buildTree(self, queue):
        while queue.qsize() > 1: 
            nodeA = queue.get()
            nodeB = queue.get()
            
            freqA, freqB = nodeA.value, nodeB.value
            
            newNode = Node('', freqA+freqB)
            newNode.left = nodeB if freqA > freqB else nodeA
            newNode.right = nodeA if freqA > freqB else nodeB

            queue.put(newNode)
        self.root = queue.get()
    
    def _buildTables(self, curr_node, path=bitarray()):
        if curr_node == None:
            return
        if curr_node.symbol != '':
            self.encodeTable[curr_node.symbol] = path
            self.decodeTable[path.to01()] = curr_node.symbol
        else:
            self._buildTables(curr_node.left, path+bitarray([0]))
            self._buildTables(curr_node.right, path+bitarray([1]))
            

        
    def encode(self, text):
        encodedText = bitarray()
        for char in text:
            encodedText += self.encodeTable.get(char)
        return encodedText
        

    def decode(self, text):
        stack = bitarray()
        decodedText = ""
        for bit in text:
            stack += bitarray([int(bit)])
            if self.decodeTable.get(stack.to01()):
                decodedText += self.decodeTable[stack.to01()]
                stack = bitarray()
        return decodedText
    

if __name__ == "__main__":
    file = open("train.txt")
    text = file.read().replace('\n', ' ')
    huff = HuffMan(text)

    if sys.argv[1] == "encode":
        eText = huff.encode(sys.argv[2])
        print(eText)
    elif sys.argv[1] == "decode":
        dText = huff.decode(sys.argv[2])
        print(dText)
    elif sys.argv[1] == "check":
        eText = huff.encode(sys.argv[2])
        dText = huff.decode(eText.to01())

        eSize = len(eText)
        dSize = len(dText)*8
        print("Encoded Size: ", eSize)
        print("Decoded Size: ", dSize)
        print("Compression Ratio: ", eSize/dSize * 100, "%")
   

