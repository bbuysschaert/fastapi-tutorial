from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date

class UserIn(BaseModel):
    email : str
    first_name : str
    last_name : str
    date_of_birth : date
    sex_at_birth : str # Should this be a special data type?

class UserOut(UserIn):
    id : int

    class Config:
        orm_model = True

