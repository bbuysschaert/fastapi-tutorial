# FastAPI  tutorial
Following along with the FastAPI tutorial from their [user guide](https://fastapi.tiangolo.com/tutorial/).

## Automatic documentation
FastAPI creates automatic OpenAPI and Swagger documentation.  The tutorial indicates that you can find these at:
- Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- OpenAPI json: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

Note: this is assuming that your application is running on the local server [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

The JSON Schemas of your [body] models will be part of your OpenAPI generated schema, and will be shown in the interactive API docs.  [Reference](https://fastapi.tiangolo.com/tutorial/body/#automatic-docs)

The function description that you add to an endpoint is passed to the Swagger documentation.  As such, it makes even more sense to provide correct documentation!!!

## Running of your FastAPI application
`>>> uvicorn main:app --reload`
where `main.py` is the main application that you want to run.


## Notes:
### Order matters
The path declarations are followed to top bottom.  This means that you need to use
```
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```
to have different behaviour for `/users/me` and `/users/{user_id}`.

It also means that only the first function declared on a path is used.

```
# This is used
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]

# This is __NOT__ used
@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]
```    

### Sending data
Use a `POST` statement instead of a `GET` statement to send data in the body of a HTTP request!!

Use [Pydantic](https://pydantic-docs.helpmanual.io/) models to declare the request body.


## Different interpretations of the function parameters
The function parameters will be recognized as follows:

- If the parameter is also declared in the __path__, it will be used as a path parameter.
- If the parameter is of a __singular type__ (like `int`, `float`, `str`, `bool`, etc) it will be interpreted as a __query__ parameter.
- If the parameter is declared to be of the type of a __Pydantic model__, it will be interpreted as a request __body__.

[Reference](https://fastapi.tiangolo.com/tutorial/body/#request-body-path-query-parameters)

## Order of arguments vs using kwargs
Standard Python behaviour enforces you that parameters without a default should be defined in a function before those with a default value.  It interprets the former as arguments, while the latter are kwargs.  This might cause some issues when declaring a mixed type of variables.  Especially when the order of your parameters matters...

FastAPI indicates that you should use a little "trick" to circumvent this problem.  Namely, define the functions as
```
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get('/items/{item_id})
async def my_func(*,
                    item_id: int = Path(),
                    q: str = Query()
                )
```

This is not suprising, as all these parameters are in essence keyword arguments...

## Declare request example data
This request example data will update the API documentations in your application.  It is different from the default values that are declared in the function / methods...  The following data types can have 

There are multiple options to declare this example data, but the main two options are:
1. In the Pydantic model as a `schema_extra;
2. As an `example` argument in the `pydantic.Field` method;
3. As an `example` argument in `fastapi.Body`, `fastapi.Path`, `fastapi.Query`, `fastapi.Header`, `fastapi.Cookie`, etc., in the function / method directly.  This method also allows multiple examples under the `examples` argument.  Which seems similar to doctesting, but without any errors thrown...

Option 1:
```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }
```

Option 2:
```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = Field(example="Foo")
    description: Union[str, None] = Field(default=None, example="A very nice Item")
    price: float = Field(example=35.4)
    tax: Union[float, None] = Field(default=None, example=3.2)
```