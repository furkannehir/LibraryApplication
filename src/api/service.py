from models import Author, Book, User, session
from schema import AuthorCreate, BookCreate, AuthorResponse, BookResponse, BookResponseForAuthor, AuthorResponseForBook, UserAuth
from auth import pwd_context
from fastapi import HTTPException


def getBooks(page: int, pageSize: int, filter: str = ''):
    books = session.query(Book).filter(Book.author_id != None).filter(Book.name.contains(filter)).offset(page*pageSize).limit(pageSize).all()
    books_response = []
    for book in books:
        books_response.append(BookResponse(
            id=book.id,
            name=book.name,
            page_number=book.page_number,
            author=AuthorResponseForBook(id=book.author.id, name=book.author.name, books=None)
        ))
    
    return books_response

def getBookById(id: int):
    book = session.query(Book).filter(Book.id == id).offset(0).limit(1).first()
    return BookResponse(
            id=book.id,
            name=book.name,
            page_number=book.page_number,
            author=AuthorResponseForBook(id=book.author.id, name=book.author.name))

def addBook(bookCreate: BookCreate):
    author = session.query(Author).filter(Author.id == bookCreate.author_id).first()

    if not author:
        return {"error": "Author not found"}

    book = Book(**bookCreate.dict(), author=author)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

def updateBook(book_id: int, book_data: BookCreate):
    book = session.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for key, value in book_data.dict().items():
        setattr(book, key, value)
    
    session.commit()
    session.refresh(book)
    
    return book

def bookCount(filter: str = ''):
    return session.query(Book).filter(Book.author_id != None).count()

def bookDelete(book_id: int):
    book = session.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    session.delete(book)
    session.commit()
    session.close()
    
    return book
    
def getAuthorById(id: int):
    author = session.query(Author).filter(Author.id == id).offset(0).limit(1).first()
    author_books = []
    for book in author.books:
        author_books.append(BookResponseForAuthor(id=book.id, name=book.name, page_number=book.page_number))
    return AuthorResponse(id=author.id, name=author.name, books=author_books)

def getAuthors(page: int, pageSize: int, filter: str = ''):
    if filter == '':
        authors = session.query(Author).offset(page*pageSize).limit(pageSize).all()
    else:
        authors = session.query(Author).filter(Author.name.contains(filter)).offset(page*pageSize).limit(pageSize).all()
    
    authors_response = []
    for author in authors:
        author_books = []
        for book in author.books:
            author_books.append(BookResponseForAuthor(id=book.id, name=book.name, page_number=book.page_number))
        
        authors_response.append(AuthorResponse(id=author.id, name=author.name, books=author_books))
    
    return authors_response

def updateAuthor(author_id: int, author_data: BookCreate):
    author = session.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    for key, value in author_data.dict().items():
        setattr(author, key, value)
    
    session.commit()
    session.refresh(author)
    
    return author
    
def addAuthor(authorCreate: AuthorCreate):
    author = Author(**authorCreate.dict())
    session.add(author)
    session.commit()
    session.refresh(author)
    session.close()
    return author

def authorCount(filter: str = ''):
    return session.query(Author).filter(Author.name.contains(filter)).count()

def deleteAuthor(author_id: int):
    author = session.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    session.delete(author)
    session.query(Book).filter(Book.author_id == author_id).delete()
    session.commit()
    session.close()
    
    return author

def createFakeUser():
    userAuth = UserAuth("admin", "password")
    user = User()
    user.username = "admin"
    user.hashed_password = pwd_context.encrypt("password")
    session.add(user)
    session.commit()
    session.refresh(user)
    return userAuth