from flask import Flask, g, request

import database_service
# from item import Item

app = Flask(__name__)


@app.before_first_request
def app_before_first_request():
    database_service.init_db()


@app.before_request
def app_before_request():
    g.db = database_service.connect_db()


@app.teardown_request
def app_teardown_request(e):
    database_service.close_db()


@app.route('/item', methods=['GET', 'POST', 'DELETE'])
def item():
    """
    1. Get current items
    2. Set (add) item
    3. Delete item

    Supported methods:

    GET: gets items from database
    POST: adds an item to the database
    DELETE: deletes an item from the database

    :return: json representation of completed action
    """

    data = []

    if request.method == 'GET':
        message = 'Successfully retrieved items'
        data = database_service.get_all_items()
    elif request.method == 'POST':
        """
        POST will add a new item to the `items` table
        """
        name = request.form.get('name')

        if name is not None:
            success = database_service.add_item(request.form.get('name'))
        else:
            success = False

        if success:
            message = 'Successfully added item'
        else:
            message = 'Unable to add item'
    elif request.method == 'DELETE':
        database_service.delete_item(request.form.get('id'))

        message = 'Successfully delete item'
    else:
        return {'success': False, 'message': 'Unimplemented HTTP method', 'data': []}, 400

    return {'success': True, 'message': message, 'data': data}, 200
