import sqlite3
from event import Event
from config import DB_PATH

def db_load() -> list[tuple]:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM event")
    events = cursor.fetchall()
    connection.close()
    return events

saved_events = db_load()
for event in saved_events:
    e = Event(event[0], event[1], event[2], event[3], event[4], [], event[6])
    print(e.body_from_text(event[5]))
    print(e)
