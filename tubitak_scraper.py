import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

from database import veritabani_olustur, duyuru_var_mi, duyuru_ekle


ANAHTAR_KELIMELER = [
    "başvuru",
    "burs",
    "staj",
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
    "teknofest",
    "çağrı",
    "destek"
]




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


veritabani_olustur()

url = "https://tubitak.gov.tr/tr/duyuru"

response = requests.get(url)

print("Durum kodu:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print("\n📢 TÜBİTAK DUYURULARI")
print("=" * 60)

ilanlar = []

for link in soup.find_all("a", href=True):

    href = link["href"]
    baslik = link.get_text(" ", strip=True)

    if "/tr/duyuru/" in href and baslik and baslik != "Devamını oku":

        tam_link = urljoin(url, href)

        if tam_link not in [x[1] for x in ilanlar]:
            ilanlar.append((baslik, tam_link))


print(f"Toplam duyuru: {len(ilanlar)}\n")


for baslik, link in ilanlar:

    metin = baslik.lower()

    ilgili_mi = any(
        kelime in metin
        for kelime in ANAHTAR_KELIMELER
    )

    if not ilgili_mi:
        print(f"🚫 İlgisiz duyuru: {baslik}")
        continue

    if duyuru_var_mi(link):

        print(f"⏭️ Daha önce görüldü: {baslik}")

    else:

        print(f"🆕 YENİ TÜBİTAK DUYURUSU: {baslik}")
        print(f"🔗 {link}")

        mesaj = f"""🔔 BAŞVURU RADARIM

🆕 Yeni TÜBİTAK duyurusu!

📌 {baslik}
🔗 {link}
"""

        telegram_bildirim_gonder(mesaj)

        duyuru_ekle(
            baslik,
            "",
            "",
            link,
            "TÜBİTAK"
        )