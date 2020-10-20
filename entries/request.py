import sqlite3
import json
from models.entry import Entry

def get_all_entries():
  with sqlite3.connect("./daily_journal.db") as conn:

    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
    SELECT
        e.id,
        e.concept,
        e.entry,
        e.date,
        e.mood_id
    FROM entries e
    """)

    entries = []

    dataset = db_cursor.fetchall()

    for row in dataset:
        entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['mood_id'])

        entries.append(entry._dict_)

  return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./daily_journal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id
        FROM entries e
        WHERE e.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        entry = Entry(data['id'], data['concept'], data['entry'], data['date'], data['mood_id'])

        return json.dumps(entry.__dict__)

def delete_entry(id):
    with sqlite3.connect("./daily_journal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))

def entries_query(query):
    my_query = '%{}%'.format(query)

    with sqlite3.connect('./daily_journal.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId
        FROM entries e
        WHERE e.entry LIKE ?
        """, (my_query,))

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['moodId'])

            entries.append(entry.__dict__)

    return json.dumps(entries)
