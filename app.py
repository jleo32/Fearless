from flask import Flask, g, request

import database_service
from utils import convert_csv_to_list

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
@app.route('/item/<item_id>', methods=['GET', 'DELETE'])
@app.route('/item/<item_id>/<name>', methods=['PUT'])
def item(item_id=None, name=None):
    """
    1. Get current items
    2. Get item by id
    3. Add items
    4. Delete item by id
    5. Delete all items
    6. Update an item

    Supported methods:

    GET: Gets items from database
         If a url parameter exists, the method will try to find an item with that id
    POST: Adds items to the database
    PUT: Updates an item in the database
    DELETE: Deletes an item from the database if id is pass; else deletes all items

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
        POST will add new items to the `items` table
        
        Acceptable body:
        
        names: name1,name2,name3
        """
        names = convert_csv_to_list(request.form.get('names', []))

        if names:
            success = database_service.add_all_items(names)
            message = 'Successfully added items'
        else:
            success = False
            message = 'Unable to add items'
            response_code = 400
    elif request.method == 'PUT':
        """
        PUT will update an item in the database
        
        Acceptable url:
        
        /item/1/name1
        """

        if item_id is not None and name is not None:
            success = database_service.update_item_by_id(item_id, name)
            message = 'Successfully updated item'
        else:
            success = False
            message = 'Unable to update item'
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
            success = database_service.delete_item_by_id(item_id)

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
