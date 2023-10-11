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


def add_subj(id: int, name: str, short: str):
    with sqlite3.Connection(connection_file) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subjects VALUES (?, ?, ?)", (id, name, short))
        conn.commit()


# print(len(subjectsjson))

def convertJsonToDB():
    try:
        for i in range(len(subjectsjson)):
            subjdat = subjectsjson[i]
            add_subj(int(subjdat["id"]), subjdat["name"], subjdat["short"])
    except Exception as ex:
        print(ex)


def deleteDB(table_name: str):
    try:
        with sqlite3.connect('your_database.db') as conn:
            cursor = conn.cursor()

            # Execute the DROP TABLE statement
            cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

            # Commit the changes and close the connection
            conn.commit()
            conn.close()
    except Exception as ex:
        print(ex)


checkDB()
