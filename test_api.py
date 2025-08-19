# test_api.py
import pytest
from fastapi.testclient import TestClient
from api import app, library
from book import Book

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_library(monkeypatch):
    """Her test öncesi kütüphaneyi temizler ve dosya yazmayı engeller."""
    library.books.clear()
    monkeypatch.setattr(library, "save_books", lambda: None)  # Dosyaya yazmayı engelle
    yield
    library.books.clear()

def test_get_books_empty():
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

def test_add_book_success(monkeypatch):
    """ISBN ile kitap ekleme başarılı senaryo."""
    def mock_add_book(isbn):
        return Book("Test Kitap", "Test Yazar", isbn)
    monkeypatch.setattr(library, "add_book", mock_add_book)

    response = client.post("/books", json={"isbn": "1234567890"})
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "title": "Test Kitap",
        "author": "Test Yazar",
        "isbn": "1234567890"
    }

def test_add_book_not_found(monkeypatch):
    """ISBN ile kitap ekleme başarısız (bulunamadı) senaryo."""
    monkeypatch.setattr(library, "add_book", lambda isbn: None)

    response = client.post("/books", json={"isbn": "0000000000"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Kitap bulunamadı veya zaten mevcut."

def test_delete_book():
    """Kitap silme senaryosu."""
    book = Book("Test Kitap", "Test Yazar", "123")
    library.books.append(book)

    response = client.delete("/books/123")
    assert response.status_code == 200
    assert response.json()["detail"] == "Kitap başarıyla silindi."
    assert len(library.books) == 0

def test_get_books_with_data():
    """GET /books ile kitap listesini alma senaryosu."""
    book1 = Book("Kitap 1", "Yazar 1", "111")
    book2 = Book("Kitap 2", "Yazar 2", "222")
    library.books.extend([book1, book2])

    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert data == [
        {"title": "Kitap 1", "author": "Yazar 1", "isbn": "111"},
        {"title": "Kitap 2", "author": "Yazar 2", "isbn": "222"}
    ]

