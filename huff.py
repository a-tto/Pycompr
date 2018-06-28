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
        self.bitcode = ''

class HuffTree:
    def __init__(self):
        self.histgram = {}
        self.leaf = {}
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
                self.leaf[x.code] = x

            if pq.empty():
                break

            y = pq.pop()
            if y.left == None and y.right == None:
                self.leaf[y.code] = y

            node = Node(None, x.count+y.count, x, y, None)
            x.parent = y.parent = node

            pq.push(node)

        self.root = x

    def encode(self, node, bitcode=''):
        if node.code != None:
            node.bitcode = bitcode
        else:
            self.encode(node=node.left, bitcode=bitcode+'0')
            self.encode(node=node.right, bitcode=bitcode+'1')

    def decode(self, node, bitcode):
        if bitcode == '' and node.code == None:
            return -1
        elif bitcode == '' and node.code != None:
            return node.code
        else:
            if bitcode[0] == '1':
                return self.decode(node.right, bitcode[1:])
            elif bitcode[0] == '0':
                return self.decode(node.left, bitcode[1:])


if __name__ == '__main__':
    tree = HuffTree()
    with open('/Users/akyo/compress/testfile', 'rb') as f:
        tree.makeHistgram(f)
    tree.makeTree()
    tree.encode(tree.root)

    print(tree.histgram)
    for k in tree.leaf:
        print('{} -> {}'.format(chr(k), tree.leaf[k].bitcode))

    print(tree.decode(tree.root, '011'))

