# Dependencies
from fastapi import FastAPI
from enum import Enum  # https://docs.python.org/3/library/enum.html

class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

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
async def read_item(item_id: int):
    """
    Return the item_id that is provided during the GET statement.
    While typing (: int) is not required during the declaration of the function, it is highly recommended.
    Typing will ensure that automatic HTTP errors are provided in case you give a string as item_id
    """
    return {'item_id': item_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

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