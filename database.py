import sqlite3

DATABASE_NAME = "basvuru_radari.db"


def veritabani_olustur():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS duyurular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baslik TEXT NOT NULL,
            tarih TEXT,
            aciklama TEXT,
            url TEXT UNIQUE NOT NULL,
            kaynak TEXT NOT NULL,
            eklenme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def duyuru_var_mi(url):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM duyurular WHERE url = ?",
        (url,)
    )

    sonuc = cursor.fetchone()

    connection.close()

    return sonuc is not None


def duyuru_ekle(baslik, tarih, aciklama, url, kaynak):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO duyurular
        (baslik, tarih, aciklama, url, kaynak)
        VALUES (?, ?, ?, ?, ?)
    """, (
        baslik,
        tarih,
        aciklama,
        url,
        kaynak
    ))

    connection.commit()
    connection.close()