# Fearless Project

Author: Justin Leo

## Overview:

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

## Caveats:

- DELETE will return success even if item id does not exist; should return a 404
- GET item by id should return a 404 if item does not exist

## Future iterations:

- More automated testing
- Update delete method to return message if item id does not exist
- Pagination for GET items
- Filter/Search endpoint for items
- Update response codes for better response handling