from flask import Flask, g, request

import database_service

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

    GET: Gets items from database
         If a url parameter exists, the method will try to find an item with that id
    POST: Adds an item to the database
    DELETE: Deletes an item from the database

    :return: json representation of completed action
    """

    success = True
    data = []
    response_code = 200

    if request.method == 'GET':
        """
        Get will retrieve all items in the `items` table
        
        If a url parameter exists, the method will try to find an item with that id
        """

        if item_id is not None:
            data = database_service.get_item_by_id(item_id)
            message = 'Successfully retrieved item'
        else:
            message = 'Successfully retrieved items'
            data = database_service.get_all_items()
    elif request.method == 'POST':
        """
        POST will add a new item to the `items` table
        """
        name = request.form.get('name')

        if name is not None:
            success = database_service.add_item(request.form.get('name'))
            message = 'Successfully added item'
        else:
            success = False
            message = 'Unable to add item'
            response_code = 400
    elif request.method == 'DELETE':
        """
        DELETE will delete an item by the id in the url parameter or delete all if none exists
        
        Note: deletion is successful even if the item id does not exist because the query was successful even
        if the row does not exist
        """
        if item_id is not None:
            """
            If the item id exists, delete the item
            """
            success = database_service.delete_item(item_id)

            if success:
                message = 'Successfully deleted item'
            else:
                message = 'Unable to delete item with id: ' + item_id
        else:
            """
            If no item id is in the url, delete all items
            """
            success = database_service.delete_all_items()

            if success:
                message = 'Successfully deleted all items'
            else:
                message = 'Unable to delete all items'
                response_code = 400
    else:
        return {'success': False, 'message': 'Unimplemented HTTP method', 'data': []}, 405

    return {'success': success, 'message': message, 'data': data}, response_code
