from typing import Union, List

from fastapi import FastAPI, Query
from pydantic import BaseModel, Required


class Item(BaseModel):
    name: str
    description: Union[str, None] = None # Is optional, note that the syntax differs for Python 3.10 and higher
    price: float
    tax: Union[float, None] = None # Is optional, note that the syntax differs for Python 3.10 and higher


app = FastAPI()

@app.get("/items2/")
async def read_items2(q: Union[str, None] = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        alias='item-query',
        min_length=3,
    )
    ):
    query_items = {"q": q}
    return query_items

@app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
        include_in_schema=False # Will not show in the OpenAPI schema, but the method and endpoint will still be visible!
        )
    ):
    """ 
    Use the Query object to give the query parameters more options!  Regular expressions or eq, lt, ... on numerical values are also possible!
    Use the ellipsis value to indicate that the query parameter is required (but if used in conjunction with "Union[str, None]" than it can be empty)
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Use a POST statement to send data
# This is no longer a GET statement!
@app.post("/items/")
async def create_item(item: Item):
    """
    Refers to the Item class, which in turn, refers to the BaseModel class from pydantic
    """
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Combining body and path parameters and query parameters
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result