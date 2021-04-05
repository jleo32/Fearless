import sqlite3
from flask import g


def init_db():
    """
    Initializes database tables for application if they do not exist.

    Should only be called once at startup.
    """

    db = connect_db()

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


def get_all_items():
    cursor = g.db.cursor()

    try:
        cursor.execute('SELECT * FROM items;')
    except Exception as e:
        print('Unable to retrieve items: ' + str(e))
        return []

    return cursor.fetchall()


def add_item(item_name):
    """
    Adds a new item with `item_name` to the `items` table

    :param item_name: String of name to add

    :return: True is insertion is successful
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


def get_item_by_id(item_id):
    pass


def delete_item(id):
    pass


def update_items(items):
    pass
