# doubly linked list
class Node:
    def __init__(self, data):
        self.next = None
        self.prev = None
        self.data = data


def traverse(head):
    # Traverse the doubly linked list and print its elements
    current = head
    while current:
      # Print current node's data
        print(current.data, end=" <-> ")
        # Move to the next node
        current = current.next
    print("None")

def insert_at_beginning(head, data):
    new_node = Node(data)
    new_node.next = head
    if head:
        head.prev = new_node
    return new_node

def unlink_last(head):
    current = head
    before_last = None
    while current:
      before_last = current
      current = current.next

    tail = before_last
    # traverse(tail)

    old_tail = tail
    if old_tail is None:
        return

    new_tail = old_tail.prev
    new_tail.next = None
    tail = new_tail
    old_tail.prev = None


def main():
    print("Hello from doubly-linked-list!")

    # Driver Code
    head = None
    head = insert_at_beginning(head, 4)
    head = insert_at_beginning(head, 3)
    head = insert_at_beginning(head, 2)
    head = insert_at_beginning(head, 1)

    traverse(head)

    unlink_last(head)
    traverse(head)

if __name__ == "__main__":
    main()
