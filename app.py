from flask import Flask, url_for

app = Flask(__name__)


@app.route('/item', methods=['GET', 'POST', 'DELETE'])
def index(request):
    """
    1. Get current items
    2. Set items
    3. Delete items

    Supported methods:

    GET: gets items from database
    POST: adds an item to the database
    DELETE: deletes an item from the database

    :param request: Request object used to perform action in API
    :return:
    """

    if request.method == 'GET':
        message = 'Successfully retrieved items'
        data = []
    elif request.method == 'POST':
        message = 'Successfully added item'
        data = []
    elif request.method == 'DELETE':
        message = 'Successfully delete item'
        data = []
    else:
        return {'success': False, 'message': 'Unimplemented HTTP method', 'data': []}, 400
    return {'success': True, 'message': message, 'data': data}, 200
