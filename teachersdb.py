import json
import sqlite3

connection_file = "main.db"
table_name = "teachers"

if __name__ == "__main__":
    with open("test.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    classesjson = data["r"]["tables"][0]["data_rows"]


def checkDB(table_name: str = table_name):
    with sqlite3.Connection(connection_file) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} 
        (id INT,
         name TEXT)''')
        conn.commit()


# To add items into the db
def add_subj(id: int, name: str, table_name: str = table_name):
    with sqlite3.Connection(connection_file) as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {table_name} VALUES (?, ?)", (id, name))
        conn.commit()


# converting the JSON-file to DB
def convertJsonToDB():
    try:
        for i in range(len(classesjson)):
            subjdat = classesjson[i]
            add_subj(int(subjdat["id"]), subjdat["short"])
    except Exception as ex:
        print(ex)


# Deleting the DB in case something changed in the NIS schedule site, so we can update our DB
def deleteDB(table_name: str = table_name):
    try:
        with sqlite3.connect(connection_file) as conn:
            cursor = conn.cursor()

            # Execute the DROP TABLE statement
            cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

            # Commit the changes and close the connection
            conn.commit()
            conn.close()
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    checkDB()
    # convertJsonToDB()
