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
    :return:
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

    cursor.execute("SELECT * FROM items")

    return cursor.fetchall()


def add_item(item):
    pass


def get_item_by_id(item_id):
    pass


def delete_item(id):
    pass


def update_items(items):
    pass
