from sqlmodel import Field, SQLModel
from pydantic import EmailStr, BaseModel
import uuid

""" Tables """
class Url(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    url: str
    user_id: uuid.UUID = Field(foreign_key="user.id")

class User(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str 
    email: EmailStr
    password: str = Field(min_length=8)

class UrlTags(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    url_id: uuid.UUID = Field(foreign_key="url.id")
    name_tag: str = Field(min_length=3)

""" Responses"""
class UrlTagsResponse(BaseModel):
    user_id: str
    url: str
    tags: list[str]

class AuthorizationResponse(BaseModel):
    user_id: uuid.UUID
    name: str
    email: EmailStr
    exp: int
    token: str | None = Field(default=None)

""" Models no tables"""
class LoginBody(BaseModel):
    email: EmailStr
    password: str

class UrlCreateSchema(BaseModel):
    url: str
    tags: list[str]

class ResponseGlobal(BaseModel):
    success: bool
    message: str
    data: AuthorizationResponse | User | Url | None 

class UpdateTagsBody(BaseModel):
    tags: list[str]