# FastAPI  tutorial
Following along with the FastAPI tutorial from their [user guide](https://fastapi.tiangolo.com/tutorial/).

## Automatic documentation
FastAPI creates automatic OpenAPI and Swagger documentation.  The tutorial indicates that you can find these at:
- Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- OpenAPI json: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

Note: this is assuming that your application is running on the local server [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

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