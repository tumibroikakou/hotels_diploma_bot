import sqlite3
import json


def db_create() -> None:
    connect = sqlite3.connect("db.sqlite3")
    cursor = connect.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
        user_id TEXT,
        hotels JSON
        )
    """)
    connect.commit()
    connect.close()


def insert_to_db(user_id: str, history: dict) -> None:
    connect = sqlite3.connect("db.sqlite3")
    cursor = connect.cursor()
    cursor.execute('SELECT user_id FROM history WHERE user_id=?', (user_id,))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO history (user_id, hotels) VALUES (?, ?)', (user_id, json.dumps(history)))
    else:
        cursor.execute('UPDATE history SET hotels=? WHERE user_id=?', (json.dumps(history), user_id))
    connect.commit()
    connect.close()


def get_from_db(user_id: str) -> None:
    result = dict()
    connect = sqlite3.connect("db.sqlite3")
    cursor = connect.cursor()
    tmp = cursor.execute('SELECT hotels FROM history WHERE user_id=?', (user_id,)).fetchone()
    if tmp:
        for i in tmp:
            result = json.loads(i)
    connect.commit()
    connect.close()
    return result
