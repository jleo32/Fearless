import sqlite3
from flask import g

from utils import convert_item_tuples


def init_db():
    """
    Initializes database table for application if they do not exist.

    Should only be called once at startup.
    """

    db = connect_db()

    cursor = db.cursor()

    with open('scheme.sql', 'r') as f:
        cursor.execute(f.read())

    db.close()


def init_test_db():
    """
    Initializes TEST database table for application if they do not exist.

    Should only be called once at startup.
    """

    try:
        db = sqlite3.connect(':memory:')
    except Exception as e:
        print('Unable to connect to database: ' + str(e))

    cursor = db.cursor()

    with open('scheme.sql', 'r') as f:
        cursor.execute(f.read())

    db.close()


def connect_db():
    """
    Created connection to the database for app context

    Database factory: db.row_factory = sqlite3.Row

    :return: Connection to local sqlite database
    """
    try:
        db = sqlite3.connect('fearless.db')
    except Exception as e:
        print('Unable to connect to database: ' + str(e))

    return db


def close_db():
    """
    Closes the connection to the database and removes the database from the app context

    https://flask.palletsprojects.com/en/1.1.x/appcontext/

    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def get_item_by_id(item_id):
    """
    Fetches item in the `items` table by `id`

    Will return an empty list if the item does not exist

    :return: List with item as dict
    """
    cursor = g.db.cursor()

    try:
        cursor.execute(f"SELECT * FROM items WHERE id = {item_id};")
    except Exception as e:
        print('Unable to retrieve item: ' + str(e))
        return []

    db_result = cursor.fetchone()

    if db_result:
        return convert_item_tuples([db_result])
    else:
        return []


def get_all_items():
    """
    Fetches all items in the `items` table

    Result from query is converted from tuples to dict

    :return: List of items as dict's
    """
    cursor = g.db.cursor()

    try:
        cursor.execute('SELECT * FROM items;')
    except Exception as e:
        print('Unable to retrieve items: ' + str(e))
        return []

    db_result = cursor.fetchall()

    return convert_item_tuples(db_result)


def add_item(item_name):
    """
    Adds a new item with `item_name` to the `items` table

    :param item_name: String of name to add

    :return: True if insertion is successful
    """
    connection = g.db
    cursor = g.db.cursor()

    try:
        cursor.execute(f"INSERT INTO items('name') VALUES ('{item_name}');")
        connection.commit()
    except Exception as e:
        print('Unable to add item: ' + str(e))
        return False
    return True


def add_all_items(items):
    """
    Adds new items to the `items` table

    :param items: list of names to add

    :return: True if insertion is successful
    """
    connection = g.db
    cursor = g.db.cursor()

    try:
        cursor.executemany("INSERT INTO items('name') VALUES (?);", items)
        connection.commit()
    except Exception as e:
        print('Unable to add items: ' + str(e))
        return False
    return True


def delete_item_by_id(item_id):
    """
    Deletes a new item with `item_id = id` to the `items` table

    :param item_id: String of id to delete

    :return: True if deletion is successful
    """
    if item_id is None:
        return False

    connection = g.db
    cursor = g.db.cursor()

    try:
        cursor.execute(f"DELETE FROM items WHERE id = '{item_id}';")
        connection.commit()
    except Exception as e:
        print('Unable to delete item: ' + str(e))
        return False
    return True


def delete_all_items():
    """
    Deletes all items in the `items` table

    :return: True if deletion is successful
    """
    connection = g.db
    cursor = g.db.cursor()

    try:
        cursor.execute('DELETE FROM items;')
        connection.commit()
    except Exception as e:
        print('Unable to delete items: ' + str(e))
        return False
    return True


def update_item_by_id(item_id, item_name):
    """
    Updates an item in the `items` table

    :param item_id: id to update
    :param item_name: new name

    :return: True if update is successful
    """
    connection = g.db
    cursor = g.db.cursor()

    try:
        cursor.execute("UPDATE items SET name = ? WHERE id = ?;", (item_name, item_id))
        connection.commit()
    except Exception as e:
        print('Unable to update item: ' + str(e))
        return False
    return True
