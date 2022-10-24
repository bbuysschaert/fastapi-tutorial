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