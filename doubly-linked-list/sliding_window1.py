# doubly linked list
class Node:
    def __init__(self, data):
        self.next = None
        self.prev = None
        self.data = data


class SlidingWindowList:
    MAX_CAPACITY = 100

    def __init__(self, capacity: int = MAX_CAPACITY):
        self.list = None
        self.size = 0
        self.capacity = capacity
        self.tail = None

    def append(self, data):
        # print(self.size)

        if self.size >= self.capacity:
            self._unlink_last()

        self.list = self._insert_at_beginning(data) # assign a new head

    def _insert_at_beginning(self, data):
        head = self.list
        new_node = Node(data)
        new_node.next = head

        if head:
            head.prev = new_node
        else:
            self.tail = new_node

        self.size += 1

        return new_node

    def _unlink_last(self):
        if self.tail is None:
            return

        old_tail = self.tail
        new_tail = old_tail.prev
        new_tail.next = None
        self.tail = new_tail
        old_tail.prev = None

        self.size -= 1

    def traverse(self):
        """Traverse the doubly linked list and print its elements"""
        current = self.list
        while current:
          # Print current node's data
            print(current.data, end=" <-> ")
            # Move to the next node
            current = current.next
        print("None")


def main():
    print("Hello from doubly-linked-list!")
    swl = SlidingWindowList(capacity=3)
    for n in range(10):
        swl.append(n)
        swl.traverse()

if __name__ == "__main__":
    main()
