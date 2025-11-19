from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class Url(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str 
    email: EmailStr
    password: str = Field(min_length=8)

