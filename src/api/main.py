from fastapi import FastAPI
import service
from schema import AuthorCreate, BookCreate, UserAuth, Token
import models
from auth import getCurrentUser, authenticateUser
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  
    "http://localhost:8080",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/login", response_model=Token)
def login_for_access_token(form_data: UserAuth):
    print(form_data)
    token_data = authenticateUser(form_data.username, form_data.password)
    if token_data is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return token_data

@app.get("/api/v1/books")
def getAllBooks(page: int = 0, pageSize: int = 100, filter: str = '', current_user: UserAuth = Depends(getCurrentUser)):
    return service.getBooks(page, pageSize, filter)

@app.get("/api/v1/book/{id}")
def getBookById(id: int, current_user: UserAuth = Depends(getCurrentUser)):
    return service.getBookById(id)

@app.post("/api/v1/book")
def addBook(book: BookCreate):
    return service.addBook(book)

@app.put("/api/v1/books/{book_id}")
def update_book(book_id: int, book_data: BookCreate, current_user: UserAuth = Depends(getCurrentUser)):
    return service.updateBook(book_id, book_data)

@app.get("/api/v1/books/count")
def update_book(filter: str = '', current_user: UserAuth = Depends(getCurrentUser)):
    return service.bookCount(filter)

@app.delete("/api/v1/books/{id}")
def deleteBook(id: int, current_user: UserAuth = Depends(getCurrentUser)):
    return service.bookDelete(id)

@app.get("/api/v1/authors")
def getAllAuthors(page: int = 0, pageSize: int = 100, filter: str = '', current_user: UserAuth = Depends(getCurrentUser)):
    return service.getAuthors(page, pageSize, filter)

@app.get("/api/v1/author/{id}")
def getAuthor(id: int, current_user: UserAuth = Depends(getCurrentUser)):
    return service.getAuthorById(id)

@app.post("/api/v1/author")
def addAuthor(author: AuthorCreate, current_user: UserAuth = Depends(getCurrentUser)):
    return service.addAuthor(author)

@app.put("/authors/{author_id}")
def update_author(author_id: int, author_data: AuthorCreate, current_user: UserAuth = Depends(getCurrentUser)):
    return service.updateAuthor(author_id, author_data)

@app.get("/api/v1/authors/count")
def update_book(filter: str = '', current_user: UserAuth = Depends(getCurrentUser)):
    return service.authorCount(filter)

@app.delete("/api/v1/authors/{id}")
def deleteAuthor(id: int, current_user: UserAuth = Depends(getCurrentUser)):
    return service.deleteAuthor(id)
    
@app.get("/create-fake-user")
def createFakeUser():
    return service.createFakeUser()