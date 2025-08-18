# library.py
import json
import os
import httpx
from book import Book

class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = [Book(**book) for book in data]
        else:
            self.books = []

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, isbn: str):
        """ISBN ile Open Library API'den kitap ekler."""
        if self.find_book(isbn):
            print("Bu ISBN'e sahip bir kitap zaten var.")
            return None

        url = f"https://openlibrary.org/isbn/{isbn}.json"
        try:
            response = httpx.get(url, timeout=5)
            if response.status_code != 200:
                print("Kitap bulunamadı.")
                return None

            data = response.json()
            title = data.get("title", "Bilinmeyen Başlık")

            authors = []
            for author in data.get("authors", []):
                author_url = f"https://openlibrary.org{author['key']}.json"
                author_res = httpx.get(author_url, timeout=5)
                if author_res.status_code == 200:
                    authors.append(author_res.json().get("name", "Bilinmeyen Yazar"))

            author_str = ", ".join(authors) if authors else "Bilinmeyen Yazar"

            book = Book(title, author_str, isbn)
            self.books.append(book)
            self.save_books()
            print("Kitap başarıyla eklendi.")
            return book

        except httpx.RequestError:
            print("İnternet bağlantısı yok veya API'ye ulaşılamıyor.")
            return None

    def remove_book(self, isbn: str):
        book = self.find_book(isbn)
        if book:
            self.books.remove(book)
            self.save_books()
            print("Kitap silindi.")
        else:
            print("Kitap bulunamadı.")

    def list_books(self):
        if not self.books:
            print("Kütüphane boş.")
            return
        for book in self.books:
            print(book)

    def find_book(self, isbn: str):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
