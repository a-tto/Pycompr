# -*- Coding: utf-8 -*-

from bitio import *
import nodepq

MAX_CODE_NUM = 256


class Node:
    def __init__(self, code, count=0, left=None, right=None, parent=None):
        self.key = count
        self.code = code
        self.count = count
        self.left = left
        self.right = right
        self.parent = parent

class Tree:
    def __init__(self):
        self.histgram = {}
        self.leaf = []
        self.root = None

    def makeHistgram(self, f):
        data = f.read()
        for c in data:
            if c not in self.histgram.keys():
                self.histgram[c] = 1
            else:
                self.histgram[c] += 1

    def makeTree(self):
        pq = nodepq.PriorityQueue()
        for k in self.histgram.keys():
            pq.push(Node(k, self.histgram[k]))

        while True:
            x = pq.pop()
            if x.left == None and x.right == None:
                self.leaf.append(x)

            if pq.empty():
                break

            y = pq.pop()
            if y.left == None and y.right == None:
                self.leaf.append(y)

            node = Node(None, x.count+y.count, x, y, None)
            x.parent = y.parent = node

            pq.push(node)

        self.root = x




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
    tree = Tree()
    with open('/Users/akyo/compress/testfile', 'rb') as f:
        tree.makeHistgram(f)
    tree.makeTree()

    for node in tree.leaf:
        print(chr(node.code) + '->' + str(node.count))
    #tree.outputNode('A')
    #tree.outputNode('B')
    #tree.outputNode('C')
    #tree.outputNode('D')


