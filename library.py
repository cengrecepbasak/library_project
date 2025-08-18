# library.py
import json
import os
from book import Book

class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        """library.json dosyasından kitapları yükler."""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = [Book(**book) for book in data]
        else:
            self.books = []

    def save_books(self):
        """Kitap listesini library.json dosyasına kaydeder."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, book: Book):
        """Yeni bir Book nesnesini ekler."""
        if self.find_book(book.isbn):
            print("Bu ISBN'e sahip bir kitap zaten var.")
            return None

        self.books.append(book)
        self.save_books()
        print("Kitap başarıyla eklendi.")
        return book

    def remove_book(self, isbn: str):
        """ISBN ile kitabı siler."""
        book = self.find_book(isbn)
        if book:
            self.books.remove(book)
            self.save_books()
            print("Kitap silindi.")
        else:
            print("Kitap bulunamadı.")

    def list_books(self):
        """Tüm kitapları listeler."""
        if not self.books:
            print("Kütüphane boş.")
            return
        for book in self.books:
            print(book)

    def find_book(self, isbn: str):
        """ISBN ile kitabı bulur."""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
