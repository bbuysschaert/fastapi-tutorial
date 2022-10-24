"""
Documentation indicates the following:

But it is still recommended to use the ideas above, using multiple classes, instead of these parameters (= response_model_include and response_model_exclude).

This is because the JSON Schema generated in your app's OpenAPI (and the docs) will still be the one for the complete model, even if you use response_model_include or response_model_exclude to omit some attributes.

This also applies to response_model_by_alias that works similarly.
"""

from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

class Song(BaseModel):
    name: str
    description: str

songs = [
    {"name": "Red", "description": "It's my aeroplane"},
    {"name": "Foo", "description": "There comes my hero"},    
]


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude=["tax"])
async def read_item_public_data(item_id: str):
    return items[item_id]

# Remember that order matters!!!
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True) # response_model_exclude_unset=True will trim the output to only key-vals where keys have been specified
async def read_item(item_id: str):
    return items[item_id]




@app.get("/songs/", response_model=List[Song])
async def read_songs():
    from operator import itemgetter
    return sorted(songs, key=itemgetter('name'))