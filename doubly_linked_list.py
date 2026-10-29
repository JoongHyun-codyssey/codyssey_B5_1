"""Mini Redis에서 사용할 이중 연결 리스트를 직접 구현한다."""

# 데이터와 다음, 이전 노드를 참조를 저장하는 노드
class Node:
    def __init__(self, data):
        self.prev = None
        self.next = None
        self.data = data


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_front(self, data):
        node = Node(data=data)
        node.next = self.head

        if self.head is None:
            self.tail = node
        else:
            self.head.prev = node

        self.head = node
        return node

    def insert_back(self, data):
        node = Node(data=data)
        node.prev = self.tail

        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node

        self.tail = node
        return node

    def remove_front(self):
        if self.head is None:
            return None

        node = self.head
        self.head = node.next

        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None

        node.prev = None
        node.next = None

        return node

    def remove_back(self):
        if self.tail is None:
            return None

        node = self.tail
        self.tail = node.prev

        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None

        node.prev = None
        node.next = None

        return node

    def remove_node(self, node):
        if node is None:
            return None

        if node is self.head:
            return self.remove_front()
        if node is self.tail:
            return self.remove_back()

        node.prev.next = node.next
        node.next.prev = node.prev

        node.prev = None
        node.next = None

        return node

    def move_to_front(self, node):
        if node is None or node is self.head:
            return node

        self.remove_node(node)

        node.next = self.head
        self.head.prev = node
        self.head = node
        return node