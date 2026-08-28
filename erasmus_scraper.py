import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

from database import (
    veritabani_olustur,
    duyuru_var_mi,
    duyuru_ekle
)

URL = "http://erasmus.mcbu.edu.tr/"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def telegram_bildirim_gonder(mesaj):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": mesaj
    }

    response = requests.post(telegram_url, data=data)

    if response.status_code == 200:
        print("📱 Telegram bildirimi gönderildi!")
    else:
        print("❌ Telegram bildirimi gönderilemedi.")
        print(response.text)


# Veritabanını oluştur
veritabani_olustur()

response = requests.get(URL, timeout=20)

print("Durum kodu:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print("\n📢 ERASMUS DUYURULARI")
print("=" * 60)

for link in soup.find_all("a", href=True):

    text = link.get_text(" ", strip=True)
    href = link["href"]

    # Sadece gerçek duyuru bağlantılarını al
    if "/Duyuru/" not in href:
        continue

    if not text or len(text) <= 10:
        continue

    tam_url = urljoin(URL, href)

    # Daha önce görüldü mü?
    if duyuru_var_mi(tam_url):
        print("⏭️ Daha önce görüldü:", text)
        continue

    print("🆕 YENİ ERASMUS DUYURUSU:", text)
    print("🔗", tam_url)

    # Veritabanına kaydet
    duyuru_ekle(
        baslik=text,
        tarih="",
        aciklama="",
        url=tam_url,
        kaynak="Erasmus"
    )

    # Telegram mesajı
    mesaj = (
        "🎓 YENİ ERASMUS DUYURUSU!\n\n"
        f"📌 {text}\n\n"
        f"🔗 {tam_url}"
    )

    telegram_bildirim_gonder(mesaj)

    print("-" * 60)