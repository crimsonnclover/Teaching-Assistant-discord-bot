from datetime import datetime


# Implementation of Min Heap, which will contains Events in Bot's class
class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, value):
        self.heap.append(value)
        self._heapify_up()

    def pop(self):
        if len(self.heap) == 0:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down()

        return root

    def _heapify_up(self):
        index = len(self.heap) - 1
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index]["dt"] < self.heap[parent_index]["dt"]:
                self.heap[index]["dt"], self.heap[parent_index]["dt"] = self.heap[parent_index]["dt"], self.heap[index]["dt"]
                index = parent_index
            else:
                break

    def _heapify_down(self):
        index = 0
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest = index

            if left_child_index < len(self.heap) and self.heap[left_child_index]["dt"] < self.heap[smallest]["dt"]:
                smallest = left_child_index

            if right_child_index < len(self.heap) and self.heap[right_child_index]["dt"] < self.heap[smallest]["dt"]:
                smallest = right_child_index

            if smallest != index:
                self.heap[index]["dt"], self.heap[smallest]["dt"] = self.heap[smallest]["dt"], self.heap[index]["dt"]
                index = smallest
            else:
                break
