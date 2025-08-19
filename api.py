# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from library import Library
from book import Book

app = FastAPI(title="Kütüphane API", description="FastAPI ile Kütüphane Servisi", version="1.0")

library = Library()

class ISBNRequest(BaseModel):
    isbn: str

class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str

@app.get("/books", response_model=list[BookResponse])
def get_books():
    """Kütüphanedeki tüm kitapları listeler."""
    return [BookResponse(title=b.title, author=b.author, isbn=b.isbn) for b in library.books]

@app.post("/books", response_model=BookResponse)
def add_book(request: ISBNRequest):
    """ISBN ile kitap ekler."""
    book = library.add_book(request.isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı veya zaten mevcut.")
    return BookResponse(title=book.title, author=book.author, isbn=book.isbn)

@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    """Belirtilen ISBN'e sahip kitabı siler."""
    book = library.find_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    library.remove_book(isbn)
    return {"detail": "Kitap başarıyla silindi."}
