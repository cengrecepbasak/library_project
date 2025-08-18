# test_library.py
import pytest
from book import Book
from library import Library

@pytest.fixture
def temp_library(tmp_path):
    test_file = tmp_path / "test_library.json"
    return Library(filename=test_file)

def test_add_book_from_api_success(monkeypatch, temp_library):
    """API başarılı yanıt döndüğünde kitap eklenmeli."""

    # ISBN sorgusunda dönecek yanıtı sahte veriyoruz
    def mock_get(url, timeout=5):
        class MockResponse:
            def __init__(self, status_code, json_data):
                self.status_code = status_code
                self._json = json_data
            def json(self):
                return self._json

        if "isbn" in url:
            return MockResponse(200, {
                "title": "Test Kitap",
                "authors": [{"key": "/authors/OL123"}]
            })
        elif "/authors/" in url:
            return MockResponse(200, {"name": "Test Yazar"})
        return MockResponse(404, {})

    monkeypatch.setattr("httpx.get", mock_get)

    result = temp_library.add_book("1234567890")
    assert result is not None
    assert result.title == "Test Kitap"
    assert result.author == "Test Yazar"

def test_add_book_api_not_found(monkeypatch, temp_library):
    """API kitap bulunamadığında None dönmeli."""

    def mock_get(url, timeout=5):
        class MockResponse:
            def __init__(self, status_code):
                self.status_code = status_code
            def json(self):
                return {}
        return MockResponse(404)

    monkeypatch.setattr("httpx.get", mock_get)

    result = temp_library.add_book("0000000000")
    assert result is None
    assert len(temp_library.books) == 0

def test_remove_book(temp_library):
    book = Book("Test", "Yazar", "1111")
    temp_library.books.append(book)
    temp_library.remove_book("1111")
    assert temp_library.find_book("1111") is None
