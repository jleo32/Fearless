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
@app.route('/item/<item_id>', methods=['GET', 'UPDATE', 'DELETE'])
def item(item_id=None):
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

    success = True
    data = []

    if request.method == 'GET':
        """
        Get will retrieve all items in the `items` table
        """
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
        """
        DELETE will delete an item by the id in the url parameter
        
        Note: deletion is successful even if the item id does not exist because the query was successful even
        if the row does not exist
        """
        success = database_service.delete_item(item_id)

        if success:
            message = 'Successfully deleted item'
        else:
            message = 'Unable to delete item with id: ' + item_id
    else:
        return {'success': False, 'message': 'Unimplemented HTTP method', 'data': []}, 400

    return {'success': success, 'message': message, 'data': data}, 200
