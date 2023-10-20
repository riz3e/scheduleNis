import json
import sqlite3

from icecream import ic

connection_file = "main.db"
table_name = "periods"

if __name__ == "__main__":
    with open("test.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    periodsjson = data["r"]["tables"][6]["data_rows"]


def checkDB(table_name: str = table_name):
    with sqlite3.Connection(connection_file) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} 
        (id INT,
         name TEXT,
         starttime TEXT, 
         endtime TEXT)''')
        conn.commit()


# To add items into the db
def add_item(id: int, name: str, starttime: str, endtime: str, table_name: str = table_name):
    with sqlite3.Connection(connection_file) as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?)", (id, name, starttime, endtime))
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
    periodsjson = data["r"]["tables"][6]["data_rows"]
    try:
        for i in range(len(periodsjson)):
            subjdat = periodsjson[i]
            add_item(int(subjdat["id"]), subjdat["name"], subjdat["starttime"], subjdat["endtime"])
    except Exception as ex:
        ic(ex, table_name)


# Deleting the DB in case something changed in the NIS schedule site, so we can update our DB
def deleteDB(table_name: str = table_name):
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


if __name__ == "__main__":
    checkDB()
    # convertJsonToDB()
