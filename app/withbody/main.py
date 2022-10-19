from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None # Is optional, note that the syntax differs for Python 3.10 and higher
    price: float
    tax: Union[float, None] = None # Is optional, note that the syntax differs for Python 3.10 and higher


app = FastAPI()


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