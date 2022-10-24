from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi_sqla import Base # -> Still check which package this is
from fastapi_sqla import Item, Session

from typing import List, Union
from structlog import get_logger
from operator import itemgetter

from models import UserIn, UserOut
from dummydata import * # bad behaviour but testing to get the "user" object out

log = get_logger()

app = FastAPI(title='app',
              )

@app.get('/health')
def health():
    """Determine whether the application is reachable"""
    return "OK"

@app.get('/v1/users', 
         response_model= List[UserOut],
         status_code= status.HTTP_200_OK
         )
def list_users(skip: int = Query(default=0, title='Skip number of users', gt=0),
               limit: int = Query(default=10, title='Number of elements per page', gt=10, le=100),
               page: int = Query(default=0, title='Page number requested', gt=0)
            ):
    """
    Retrieve an ordered list of users.  Ordering happens on the last_name of the user
    """
    users = sorted(users, key=itemgetter('last_name'))
    # Pagination magic -> needs separate function
    return users

@app.post('/v1/users')
def create_users(user: UserIn):
    pass

@app.get('/v1/user/{user_id}',
        response_model= UserOut
        )
def get_user(user_id: int):
    """
    Retrieve a single user based on the unique user ID
    """
    user = [uu for uu in users if uu['id'] == user_id]
    if len(user) == 1:
        return user[0]
    else:
        raise HTTPException(404, 'User not found')
