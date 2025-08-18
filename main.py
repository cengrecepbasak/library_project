# main.py
from book import Book
from library import Library

def main():
    library = Library()

    while True:
        print("\n--- Kütüphane Uygulaması ---")
        print("1. Kitap Ekle (ISBN ile)")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        choice = input("Seçiminiz: ")

        if choice == "1":
            isbn = input("Kitap ISBN numarası: ")
            book = library.add_book(isbn)
            if book:
                print(f"Kitap eklendi: {book}")
            else:
                print("Kitap eklenemedi veya bulunamadı.")

        elif choice == "2":
            isbn = input("Silinecek kitabın ISBN numarası: ")
            library.remove_book(isbn)

        elif choice == "3":
            library.list_books()

        elif choice == "4":
            isbn = input("Aranacak kitabın ISBN numarası: ")
            book = library.find_book(isbn)
            if book:
                print(book)
            else:
                print("Kitap bulunamadı.")

        elif choice == "5":
            print("Çıkılıyor...")
            break

        else:
            print("Geçersiz seçim. Tekrar deneyin.")

if __name__ == "__main__":
    main()

