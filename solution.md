# Fearless Project

Author: Justin Leo

## Overview:

The simple application allows a user to add, delete, and retrieve items from a persistent SQL database.

## Technologies

- Python 3.8
- Flask 1.1.2
- SQLite
- Postman
- Docker

## How to:

To build the docker container, run:

```shell
docker build --tag fearless .
```

To run the docker container on port 3000, run:

```shell
docker run -d -p 3000:3000 fearless
```

For easier startup, `start_app.sh` was created to build and run the application in one command:

```shell
chmod +x start_app.sh  # if applicable

./start_app.sh 

# or

sh start_app.sh
``` 

This will startup the application and is accessible at:

http://127.0.0.1:3000/item

or possibly

http://0.0.0.0:3000/item

## API:

### GET

`/item` - Retrieves all items in the database

`/item/<item_id>` - Retrieves the item with the specified id, empty list if it does not exist

Example: `GET - /item/1`

### POST

`/item` - Adds list of names to database

Body: `names: <comma separated list of names>`

Example: `POST - names: name1,name2,name3`

### PUT

`/item/<item_id>/<name>` - Updates item with new name by id

Example: `PUT - /item/1/name1`

### DELETE

`/item` - Deletes all items in the database

`/item/<item_id>` - Deletes an item with the specified id

Example: `DELETE - /item/1`


## Caveats:

- DELETE will return success even if item id does not exist; should return a 404
- GET will return success even if item id does not exist; should return a 404
- PUT item will return success even if the item id does not exist; should return a 404

## Future iterations:

- More automated testing
- Update delete method to return message if item id does not exist
- Pagination for GET items
- Filter/Search endpoint for items
- Update response codes for better response handling
- Data return value should be removed for some methods if it's not applicable