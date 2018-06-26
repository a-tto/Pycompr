
def heapsort_one_step(heaplist,child_pos):
    if child_pos == 0:
        return heaplist,0,-1
    child = heaplist[child_pos]
    parent_pos = (child_pos-1)//2
    parent = heaplist[parent_pos]
    if parent.key > child.key:
        heaplist[child_pos], heaplist[parent_pos] = parent,child
        return heaplist,parent_pos,1
    else:

        return heaplist,parent_pos,-1

def heapsort(heaplist):
    a = 1
    child_pos = len(heaplist)-1
    while a != -1:
        heaplist,child_pos,a = heapsort_one_step(heaplist,child_pos)
    return heaplist

def key_func(n):
    return n.key

def reconstruct_heap_one_step(heaplist,parent_pos):

    if len(heaplist) == 2:
        heaplist = [min(heaplist, key=key_func),max(heaplist, key=key_func)]
        return heaplist, parent_pos, -1

    if 2*parent_pos+2 > len(heaplist)-1:
        return heaplist, parent_pos,-1

    child1 = heaplist[2*parent_pos + 1]
    child2 = heaplist[2*parent_pos + 2]

    if child1.key > child2.key:
        minchild = child2
        child_pos = 2*parent_pos + 2
    else:
        minchild = child1
        child_pos = 2*parent_pos + 1

    if heaplist[parent_pos].key > minchild.key:
        heaplist[child_pos], heaplist[parent_pos] = heaplist[parent_pos],heaplist[child_pos]
        return heaplist, child_pos,1
    else:
        return heaplist,child_pos,-1

def reconstruct_heap(heaplist):
    a = 1
    parent_pos = 0
    while a != -1:
        heaplist, parent_pos, a = reconstruct_heap_one_step(heaplist,parent_pos)
    return heaplist

class PriorityQueue:
    def __init__(self, node=[]):
        self.node = node

    def push(self, item):
        self.node.append(item)
        self.node = heapsort(self.node)

    def pop(self):
        popval = self.node[0]
        self.node[0] = self.node[-1]
        self.node = self.node[:-1]
        self.node = reconstruct_heap(self.node)
        return popval

    def empty(self):
        if len(self.node) == 0:
            return True
        else:
            return False

if __name__ == '__main__':
    pq = PriorityQueue()
    pq.push(huff.Node('A', 12))
    print(pq.pop().code)
