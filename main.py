from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import database
import models

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

class BookCreate(BaseModel):
    code: str
    title: str
    price: float
    pages: int

@app.get("/")
def root():
    return {"message": "API đang chạy", "data": None}

@app.get("/books", status_code= status.HTTP_200_OK, tags= ["Books"])
def get_books(db : Session = Depends(database.get_db)):
    book_db = db.query(models.BookModel).all() 
    if not book_db:
        raise HTTPException (
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Book Not Found!"
        )
    return book_db

@app.post("/books", status_code= status.HTTP_201_CREATED, tags= ["Books"])
def add_book(book : BookCreate, db : Session = Depends(database.get_db)):
    try:
        new_book = models.BookModel(
            code = book.code,
            title = book.title,
            price = book.price,
            pages = book.pages
        )

        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        return {
            "status_code": status.HTTP_201_CREATED,
            "message": "Thêm thành công!",
            "data": new_book
        }
    except SQLAlchemyError as s:
        db.rollback()       
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= f"{s}"
        )