class LinkedList:
    def __init__(self, root):
        self.root = root
        self.tail = root

    def to_string(self):
        s = ""
        root = self.root

        if root is None:
            return s

        if isinstance(root.value, bytes):
            s = b''

        while root is not None:
            s += root.value
            root = root.next
        return s

    def add(self, node):
        if self.root is None:
            self.root = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node


class Node:
    def __init__(self, value, _next):
        self.value = value
        self.next = _next