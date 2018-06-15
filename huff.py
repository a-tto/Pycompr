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

    def __cmp__(x,y):
        return x.count - y.count

class HuffTree:
    def __init__(self,treesize):
        self.treesize = treesize
        self.left = [0] * 2 * MAX_CODE_NUM
        self.right = [0] * 2 * MAX_CODE_NUM
        self.parent = [0] * 2 * MAX_CODE_NUM
        self.histgram = [0] * 2 * MAX_CODE_NUM

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
            h[self.treesize] = h[d1] + h[d2]
            self.treesize += 1
            del h[d1]
            if d1 < d2:
                del h[d2 - 1]
            else:
                del h[d2]

    def outputHuffEncode(self, value):
        code = []
        c = 0
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

        #index 0 から１ビット単位で出力するように呼び出し元で制御する
        return code.reverse()



def getTwoMinIndex(histgram):
    m1 = min(histgram)
    d1 = histgram.index(m1)
    histgram[d1] = MAX_CODE_NUM + 1
    m2 = min(histgram)
    d2 = histgram.index(m2)
    histgram[d1] = m1

    return d1,d2



