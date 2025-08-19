Kütüphane API Projesi

Bu proje, Python 202 Bootcamp kapsamında geliştirilmiş bir kütüphane yönetim sistemidir. Uygulama, nesne yönelimli programlama (OOP) prensiplerini, harici API entegrasyonunu ve FastAPI kullanarak web servisi oluşturmayı kapsamaktadır.

Kullanıcılar, sisteme kitap ekleyebilir, mevcut kitapları silebilir ve kütüphanedeki tüm kitapları listeleyebilir. Kitap ekleme işlemi, yalnızca ISBN numarası kullanılarak Open Library API üzerinden otomatik olarak gerçekleştirilir.

📂 Proje Yapısı
library_project/
│
├─ api.py           # FastAPI uygulaması
├─ library.py       # Library sınıfı
├─ book.py          # Book sınıfı
├─ library.json     # Kalıcı veri dosyası
├─ requirements.txt # Python bağımlılıkları
├─ test_library.py  # Pytest testleri
├─ test_api.py      # Pytest API testleri
├─ main.py          # Terminal uygulaması

📥 Kurulum

Projeyi bilgisayarınıza klonlayın:

git clone https://github.com/cengrecepbasak/library_project.git
cd library_project

Sanal Ortam (Opsiyonel ama tavsiye edilir)
python -m venv venv
.\venv\Scripts\activate       # Windows
source venv/bin/activate      # Mac/Linux


Gerekli bağımlılıkları yükleyin:

pip install -r requirements.txt


Eğer FastAPI veya httpx yüklü değilse ayrı yükleyebilirsiniz:

pip install fastapi uvicorn httpx

💻 Kullanım
1. Terminal Uygulaması (Aşama 1 & 2)
python main.py


Örnek menü:

--- Kütüphane Uygulaması ---
1. Kitap Ekle (ISBN ile)
2. Kitap Sil
3. Kitapları Listele
4. Kitap Ara
5. Çıkış

2. FastAPI Uygulaması (Aşama 3)

API sunucusunu başlatmak için:

uvicorn api:app --reload


Tarayıcıda http://127.0.0.1:8000/docs adresine giderek Swagger UI üzerinden API’yi test edebilirsiniz.

🛠 API Dokümantasyonu

GET /books
Kütüphanedeki tüm kitapları döner.

Örnek yanıt:

[
  {
    "title": "Nutuk",
    "author": "Mustafa Kemal Atatürk",
    "isbn": "9789750802365"
  }
]


POST /books
ISBN alır, Open Library API’den bilgileri çekip kütüphaneye ekler.

İstek:

{
  "isbn": "9789750802365"
}


Yanıt:

{
  "title": "Nutuk",
  "author": "Mustafa Kemal Atatürk",
  "isbn": "9789750802365"
}


DELETE /books/{isbn}
Belirtilen ISBN’e sahip kitabı siler.

Yanıt:

{
  "detail": "Kitap başarıyla silindi."
}

✅ Testler

Tüm testleri çalıştırmak için:

pytest