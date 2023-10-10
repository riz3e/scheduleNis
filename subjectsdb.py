import json
import sqlite3

connection_file = "main.db"

with open("test.json", 'r', encoding='utf-8') as file:
    data = json.load(file)
subjectsjson = data["r"]["tables"][1]["data_rows"]


def checkDB():
    with sqlite3.Connection(connection_file) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS subjects 
        (id INT,
         name TEXT,
         short TEXT)''')
        conn.commit()


def add_subj(id: str, name: str, short: str):
    with sqlite3.Connection(connection_file) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders VALUES (?, ?, ?)", (id, name, short))
        conn.commit()
# print(len(subjectsjson))
for i in range(len(subjectsjson)):
    # print(subjectsjson[i])
    subjdat = subjectsjson[i]


checkDB()
