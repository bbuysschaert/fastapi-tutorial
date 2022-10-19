# FastAPI  tutorial
Following along with the FastAPI tutorial from their [user guide](https://fastapi.tiangolo.com/tutorial/).

## Automatic documentation
FastAPI creates automatic OpenAPI and Swagger documentation.  The tutorial indicates that you can find these at:
- Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- OpenAPI json: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

Note: this is assuming that your application is running on the local server [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

The JSON Schemas of your [body] models will be part of your OpenAPI generated schema, and will be shown in the interactive API docs.  [Reference](https://fastapi.tiangolo.com/tutorial/body/#automatic-docs)

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
