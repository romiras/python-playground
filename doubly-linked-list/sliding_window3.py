from typing import Callable, NamedTuple

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

    def append(self, data: str):
        removed_id = None
        if self.size >= self.capacity:
            self._unlink_last()

        self.list = self._insert_at_beginning(data) # assign a new head
        return removed_id

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
        if self.size == 1:
            # Single node: clear both head and tail
            self.list = None
            self.tail = None
            self.size -= 1
            old_tail.prev = None  # for explicit detachment
            return

        # Multi-node case
        new_tail = old_tail.prev
        new_tail.next = None
        self.tail = new_tail
        old_tail.prev = None
        self.size -= 1

    def nodes(self):
        """Traverse the doubly linked list and yield its elements"""
        current = self.list
        while current:
            yield current.data
            # Move to the next node
            current = current.next

    def traverse(self):
        """Traverse the doubly linked list and print its elements"""
        current = self.list
        print("DEBUG: ", end="")
        while current:
          # Print current node's data
            print(current.data, end=" <-> ")
            # Move to the next node
            current = current.next
        print("None")


class UserActivity(NamedTuple):
    user_id: str


class SuspiciousActivityDetector:
    WINDOW_SIZE = 3
    ALERTING_NUM_OCCURRENCES = 2

    def __init__(self, alert_callback: Callable[[str], None], window_size: int = WINDOW_SIZE):
        self.window_size = window_size
        self.activities = SlidingWindowList(capacity=window_size)
        self.alert_callback = alert_callback
        self.counts: dict[str, int] = {}

    def add(self, user_id: str) -> None:
        if not isinstance(user_id, str) or user_id is None or not user_id.strip():  # Basic sanity: non-empty str
            print(f"Invalid user_id: {user_id} - skipping.")
            return  # Or raise ValueError("user_id must be a non-empty string")

        print(f"- {user_id} logged-in")
        removed_id = self.activities.append(user_id)
        if removed_id:
            self.counts[removed_id] = self.counts.get(removed_id, 1) - 1
            if self.counts[removed_id] == 0:
                del self.counts[removed_id]  # Clean up zero counts

        self.counts[user_id] = self.counts.get(user_id, 0) + 1

        if self.counts[user_id] >= self.ALERTING_NUM_OCCURRENCES:
            self.alert_callback(user_id)

        self.activities.traverse()

        if self._get_occurrences(user_id) >= self.ALERTING_NUM_OCCURRENCES:
            self.alert_callback(user_id)


    def _get_occurrences(self, user_id: str) -> int:
        return self.counts.get(user_id, 0)  # O(1) lookup!


def alert(user_id: str) -> None:
    print(f"WARNING! User {user_id} has a suspicious activity!")

# We want to trigger event `user_login_alerts` if `user_id` in current event appeared N or more times in last 100 events of stream in real time.
def process_events(user_logins):
    user_logins_list = SuspiciousActivityDetector(alert_callback=alert)

    for user_login in user_logins:
        user_logins_list.add(user_login.user_id)


def main():
    print("Real time event processor")

    user_logins = [
        UserActivity(user_id='Tom'),
        UserActivity(user_id='Bob'),
        UserActivity(user_id='Alice'),
        UserActivity(user_id='Tom'),
        UserActivity(user_id='Frank'),
        UserActivity(user_id='Bob'),
        UserActivity(user_id='Alice'),
        UserActivity(user_id='Bob'),
        UserActivity(user_id='Frank'),
    ]
    process_events(user_logins)

if __name__ == "__main__":
    main()
