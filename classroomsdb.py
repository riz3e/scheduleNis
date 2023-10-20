import json
import sqlite3

from icecream import ic

connection_file = "main.db"
table_name = "classrooms"

if __name__ == "__main__":
    with open("test.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    classroomsjson = data["r"]["tables"][2]["data_rows"]


def checkDB(table_name: str = table_name):
    with sqlite3.Connection(connection_file) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} 
        (id INT,
         short TEXT)''')
        conn.commit()


# To add items into the db
def add_item(id: int, short: str, table_name: str = table_name):
    with sqlite3.Connection(connection_file) as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {table_name} VALUES (?, ?)", (id, short))
        conn.commit()


# param - responsible for the column name, value - is value of the specific param
def get_item(param: str, value):
    with sqlite3.Connection(connection_file) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE {param} = ?", (value,))
        item = cursor.fetchone()
        return item


# converting the JSON-file to DB
def convertJsonToDB(path: str = "data/maindbi.json"):
    """

    :param path: path to main db json
    :return:
    """
    with open(path, 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    classroomsjson = data["r"]["tables"][2]["data_rows"]
    try:
        for i in range(len(classroomsjson)):
            subjdat = classroomsjson[i]
            add_item(int(subjdat["id"]), subjdat["short"])
    except Exception as ex:
        ic(ex, table_name)


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
