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

    def insert_front(self, data)-> Node:
        node = Node(data=data)
        node.next = self.head

        if self.head is None:
            self.tail = node
        else:
            self.head.prev = node

        self.head = node
        return node

    def insert_back(self, data) -> Node:
        node = Node(data=data)
        node.prev = self.tail

        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node

        self.tail = node
        return node