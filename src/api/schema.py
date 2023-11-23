from typing import List
from pydantic import BaseModel


class AuthorCreate(BaseModel):
    name: str

class BookResponseForAuthor(BaseModel):
    id: int
    name: str
    page_number: int
    
class AuthorResponseForBook(BaseModel):
    id: int
    name: str
    
class AuthorResponse(BaseModel):
    id: int
    name: str
    books: List[BookResponseForAuthor]

class BookCreate(BaseModel):
    name: str
    page_number: int
    author_id: int

class BookResponse(BaseModel):
    id: int
    name: str
    page_number: int
    author: AuthorResponseForBook

class Token(BaseModel):
    access_token: str
    token_type: str

class UserAuth(BaseModel):
    username: str
    password: str