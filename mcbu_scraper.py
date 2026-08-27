import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from database import veritabani_olustur, duyuru_var_mi, duyuru_ekle


# Telegram bilgileri
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# Telegram'a bildirim gönder
def telegram_bildirim_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": mesaj
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("📱 Telegram bildirimi gönderildi!")
    else:
        print("❌ Telegram bildirimi gönderilemedi.")
        print(response.text)


# İlgili duyuruları bulmak için anahtar kelimeler
ANAHTAR_KELIMELER = [
    "başvuru",
    "erasmus",
    "burs",
    "staj",
    "part-time",
    "yarışma",
    "yarışması",
    "proje",
    "program",
    "gönüllü",
    "gönüllülük",
    "iş ilanı",
    "istihdam",
    "kariyer",
    "hackathon",
    "teknofest"
]


# Veritabanını oluştur
veritabani_olustur()


# CBÜ ana sayfası
url = "https://www.mcbu.edu.tr/"


# Siteye bağlan
response = requests.get(url)

print("Durum kodu:", response.status_code)


# HTML'i analiz et
soup = BeautifulSoup(response.text, "html.parser")


# Duyurular bölümünü bul
duyurular = soup.find(id="duyurular-tab-pane")


print("\n📢 CBÜ DUYURULARI")
print("=" * 60)


if duyurular:

    ilanlar = duyurular.select("a.mini-box-link")

    print(f"Toplam duyuru: {len(ilanlar)}\n")


    for i, ilan in enumerate(ilanlar, start=1):

        # Başlık
        baslik_element = ilan.find("h6")

        baslik = (
            baslik_element.get_text(" ", strip=True)
            if baslik_element
            else "Başlık yok"
        )


        # Tarih
        tarih_element = ilan.select_one("span.new")

        tarih = (
            tarih_element.get_text(" ", strip=True)
            if tarih_element
            else "Tarih yok"
        )


        # Açıklama
        aciklama_element = ilan.find("p")

        aciklama = (
            aciklama_element.get_text(" ", strip=True)
            if aciklama_element
            else ""
        )


        # Duyuru bizim için ilgili mi?
        metin = (baslik + " " + aciklama).lower()

        ilgili_mi = any(
            kelime in metin
            for kelime in ANAHTAR_KELIMELER
        )


        # Link
        link = ilan.get("href", "")

        link = urljoin(url, link)


        # İlgili değilse geç
        if not ilgili_mi:
            print(f"🚫 İlgisiz duyuru: {baslik}")
            continue


        # Daha önce kayıt edilmiş mi?
        if duyuru_var_mi(link):

            print(f"⏭️ Daha önce görüldü: {baslik}")

        else:

            print(f"🆕 YENİ DUYURU: {baslik}")
            print(f"   📅 {tarih}")
            print(f"   🔗 {link}")


            # Telegram mesajı
            mesaj = f"""🔔 BAŞVURU RADARIM

🆕 Yeni CBÜ duyurusu!

📌 {baslik}
📅 {tarih}
🔗 {link}
"""


            # Telegram'a gönder
            telegram_bildirim_gonder(mesaj)


            # Veritabanına kaydet
            duyuru_ekle(
                baslik,
                tarih,
                aciklama,
                link,
                "Manisa Celal Bayar Üniversitesi"
            )


else:

    print("❌ Duyurular bölümü bulunamadı.")