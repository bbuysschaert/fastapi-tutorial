from typing import Union, List, Dict

from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from pydantic import BaseModel, Required, Field, HttpUrl


class Item(BaseModel):
    name: str
    description: Union[str, None] = None # Is optional, note that the syntax differs for Python 3.10 and higher
    price: float
    tax: Union[float, None] = None # Is optional, note that the syntax differs for Python 3.10 and higher

    # Declare request example data
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

class Image(BaseModel):
    url: HttpUrl
    name: str


app = FastAPI()

@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    """
    Use a nested data type; a list of Image models
    """
    return images

@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    """
    Accept any dict as long as it has int keys with float values
    
    Have in mind that JSON only supports str as keys.
    But Pydantic has automatic data conversion.
    This means that, even though your API clients can only send strings as keys, as long as those strings contain pure integers, Pydantic will convert them and validate them.
    """
    return weights

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

@app.get("/items2/")
async def read_items2(
    q: Union[str, None] = Query(
            default=None,
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            alias='item-query',
            min_length=3,
            ),
    ads_id: Union[str, None] = Cookie(default=None),
    user_agent = Union[str, None] = Header(default=None)):
    """
    Some documentation
    """
    query_items = {"q": q}
    query_items.update({'ads_id':ads_id})
    query_items.update({'User-Agent':user_agent})
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
        include_in_schema=True # Will not show this parameter in the OpenAPI schema if False, but the method and endpoint will still be visible!
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

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
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
"""
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
"""