import sqlite3

from config import DB_PATH


# Implementation of Min Heap, which will contains Events in Bot's class, easy to add events and get min date events
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


    def remove(self, id):
        for i in range(len(self.heap)):
            if self.heap[i].id == id:
                self.heap.pop(i)
                break
        self.heapify()


    def heapify(self):
        n = len(self.heap)
        start_index = (n // 2) - 1
        for i in range(start_index, -1, -1):
            self._heapify_down(i)


    def _heapify_up(self):
        index = len(self.heap) - 1
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index].dt < self.heap[parent_index].dt:
                self.heap[index].dt, self.heap[parent_index].dt = self.heap[parent_index].dt, self.heap[index].dt
                index = parent_index
            else:
                break


    def _heapify_down(self, index=0):
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest = index

            if left_child_index < len(self.heap) and self.heap[left_child_index].dt < self.heap[smallest].dt:
                smallest = left_child_index

            if right_child_index < len(self.heap) and self.heap[right_child_index].dt < self.heap[smallest].dt:
                smallest = right_child_index

            if smallest != index:
                self.heap[index].dt, self.heap[smallest].dt = self.heap[smallest].dt, self.heap[index].dt
                index = smallest
            else:
                break


def db_init():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS event
                  (id TEXT PRIMARY KEY, guild INTEGER, channel INTEGER, type TEXT, header TEXT, body TEXT, date_time TEXT)
                    ''')
    connection.commit()
    connection.close()


def db_load() -> list[tuple]:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM event")
    events = cursor.fetchall()
    connection.close
    return events


def db_remove_by_id(id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM event WHERE id = ?", (id,))
    connection.commit()
    connection.close()


def db_append(event):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    body = event.body_to_text()
    cursor.execute("INSERT INTO event (id, guild, channel, type, header, body, date_time) VALUES (?, ?, ?, ?, ?, ?, ?)", (event.id, event.guild, event.channel, event.type, event.header, body, event.dt))
    connection.commit()
    connection.close()


def db_get_by_channel(channel: int) -> list[tuple]:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM event WHERE channel = ?", (channel,))
    events = cursor.fetchall()
    connection.close
    return events
