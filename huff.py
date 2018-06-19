from bitio import *
import queue
import heapq

MAX_CODE_NUM = 256


class Node:
    def __init__(self, code, count=0, left=None, right=None):
        self.code = code
        self.count = count
        self.left = left
        self.right = right

class HuffTree:
    def __init__(self, treesize, filename):
        self.treesize = treesize
        self.left = [0] * 2 * MAX_CODE_NUM
        self.right = [0] * 2 * MAX_CODE_NUM
        self.parent = [0] * 2 * MAX_CODE_NUM
        self.histgram = []
        with open(filename, 'rb') as f:
            self.makeHistgram(f)
            self.makeHuffTree()


    def makeHistgram(self, f):
        data = f.read()
        for c in data:
            if c < 0 or c > MAX_CODE_NUM:
                return -1
            self.histgram[c] += 1


    def makeHuffTree(self):
        h = self.histgram
        while True:
            if len(h) <= 1:
                break
            d1, d2 = getTwoMinIndex(h)

            self.left[self.treesize] = d1
            self.right[self.treesize] = d2
            self.parent[d1] = self.treesize
            self.parent[d2] = -self.treesize
            h.append(h[d1] + h[d2])
            self.treesize += 1
            del h[d1]
            if d1 < d2:
                del h[d2 - 1]
            else:
                del h[d2]

    def outputEncode(self, out_bit_f, in_f):
        code = []
        c = 0

        for i in range(len(in_f)):
            value = ord(in_f.read(1))
            nowNode = value

            while True:
                selectBranch = self.parent[nowNode] > 0
                nextNode = abs(self.parent[nowNode])
                if selectBranch:
                    code.append(0)
                else:
                    code.append(1)

                if nextNode == self.treesize - 1:
                    break
                nowNode = nextNode

            code.reverse()

            for bit in code:
                out_bit_f.putbit(bit)

    def outputNode(self, node):
        code = []
        nowNode = ord(node)
        while True:
            selectBranch = self.parent[nowNode] > 0
            nextNode = abs(self.parent[nowNode])
            if selectBranch:
                code.append(0)
            else:
                code.append(1)

            if nextNode == self.treesize - 1:
                break
            nowNode = nextNode

        code.reverse()

        print(code)



def getTwoMinIndex(histgram):
    m1 = min(histgram)
    d1 = histgram.index(m1)
    histgram[d1] = MAX_CODE_NUM*3 + 1
    m2 = min(histgram)
    d2 = histgram.index(m2)
    histgram[d1] = m1

    return d1,d2

if __name__ == '__main__':
    tree = HuffTree(MAX_CODE_NUM, '/Users/akyo/compress/testfile')

    tree.outputNode('A')
    tree.outputNode('B')
    tree.outputNode('C')
    tree.outputNode('D')


