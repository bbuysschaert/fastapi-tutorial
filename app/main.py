# Dependencies
from fastapi import FastAPI
from enum import Enum  # https://docs.python.org/3/library/enum.html
from typing import Union

# Variables that have been declared during the tutorial
class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# Declare the app
app = FastAPI()

# Declare the paths
@app.get('/')
async def root():
    """
    Basic function that automatically returns the json below
    """
    return {'message': 'Hello World'}

@app.get('/items/{item_id}')
async def read_item(item_id: int, q: Union[str, None] = None, short: bool = False):
    """
    Return the item_id that is provided during the GET statement.
    While typing (: int) is not required during the declaration of the function, it is highly recommended.
    Typing will ensure that automatic HTTP errors are provided in case you give a string as item_id
    """
    item = {"item_id": item_id}
    if q:
        item.update({'q':q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
    
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):
    """
    You can combine this with the earlier defined /users/{user_id}
    """
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """
    Different equality formatting is used.  Was used as such in the example
    """
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """
    https://fastapi.tiangolo.com/tutorial/path-params/#path-convertor
    Note: however, that this is dangerous behaviour
    """
    return {"file_path": file_path}

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    """
    The query parameters at the endpoint /items/ are declared in the function.
    Their datatype are included through typing in the function!
    Their default values are included.  Meaning that `http://127.0.0.1:8000/items/` results in 'http://127.0.0.1:8000/items/?skip=0&limit=10`.
    Pure optional parameters need to get a `None` as default
    You can also make them in regular (and required) arguments by not providing any default values
    """
    return fake_items_db[skip : skip + limit]