from bitio import *
import queue

class Node:
    def __init__(self, code, count=0, left=None, right=None):
        self.code = code
        self.count = count
        self.left = left
        self.right = right

    def __cmp__(x,y):
        return x.count - y.count
