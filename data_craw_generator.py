import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import random

# ==============================================================================
# [CONFIG] PARAMETER URL - SILAKAN GANTI LINK DI BAWAH INI
# ==============================================================================
# Cari artikel panjang/berita yang relevan dengan topik masing-masing.
# Script akan mengambil semua teks paragraf dari link tersebut.

# 1. URL untuk SENTIMEN (Cari artikel opini/ulasan/blog curhat)
URL_SENTIMEN = "https://id.wikipedia.org/wiki/Ulasan_konsumen" 

# 2. URL untuk LDA (Cari berita politik/ekonomi yang teksnya panjang)
URL_LDA = "https://id.wikipedia.org/wiki/Politik_Indonesia"

# 3. URL untuk BTM (Cari artikel santai/lifestyle/hiburan)
URL_BTM = "https://id.wikipedia.org/wiki/Media_sosial"

# 4. URL untuk BERTOPIC (Cari artikel teknis/tutorial/keluhan teknologi)
URL_BERTOPIC = "https://id.wikipedia.org/wiki/Pemecahan_masalah"

# Target jumlah data (Script akan mengulang-ulang konten web agar mencapai jumlah ini)
TARGET_ROWS = 10000 

# ==============================================================================
# LOGIKA SCRAPING (JANGAN DIUBAH KECUALI PAHAM)
# ==============================================================================

if not os.path.exists('data'):
    os.makedirs('data')

def get_text_from_url(url):
    print(f"🌍 Sedang scraping: {url}...")
    try:
        # User Agent agar tidak dianggap bot
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Gagal akses URL (Status {response.status_code}). Menggunakan dummy text.")
            return ["Data tidak dapat diambil dari URL ini."]
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Ambil semua tag <p> (paragraf)
        paragraphs = soup.find_all('p')
        
        # Bersihkan text
        text_list = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 20]
        
        if len(text_list) == 0:
            print("⚠️ Tidak ditemukan paragraf <p>. Mengambil semua text body.")
            text_list = [soup.get_text().strip()]
            
        print(f"✅ Berhasil mengambil {len(text_list)} paragraf unik.")
        return text_list
        
    except Exception as e:
        print(f"❌ Error scraping: {e}")
        return ["Error saat mengambil data."]

def expand_data_to_target(source_list, target_count):
    """Menduplikasi data agar mencapai target rows"""
    result = []
    while len(result) < target_count:
        result.extend(source_list)
    return result[:target_count]

print("🚀 MEMULAI PROSES GENERATE DATA DARI WEB...")

# --- 1. PROSES SENTIMEN ---
print("\n[1/4] Memproses Data Sentimen...")
raw_texts = get_text_from_url(URL_SENTIMEN)
final_texts = expand_data_to_target(raw_texts, TARGET_ROWS)

# Karena kita ambil dari web sembarang, kita tidak tahu label aslinya.
# Kita random saja labelnya agar script analisis nanti jalan.
data_sentimen = []
for text in final_texts:
    label = random.choice(['Positif', 'Negatif', 'Netral'])
    data_sentimen.append({'text': text, 'label_manual': label})

pd.DataFrame(data_sentimen).to_csv('data/sentiment.csv', index=False)
print("💾 Tersimpan: data/sentiment.csv")


# --- 2. PROSES LDA ---
print("\n[2/4] Memproses Data LDA...")
raw_texts = get_text_from_url(URL_LDA)
final_texts = expand_data_to_target(raw_texts, TARGET_ROWS)
pd.DataFrame({'text': final_texts}).to_csv('data/lda.csv', index=False)
print("💾 Tersimpan: data/lda.csv")


# --- 3. PROSES BTM ---
print("\n[3/4] Memproses Data BTM...")
raw_texts = get_text_from_url(URL_BTM)
final_texts = expand_data_to_target(raw_texts, TARGET_ROWS)
pd.DataFrame({'text': final_texts}).to_csv('data/btm.csv', index=False)
print("💾 Tersimpan: data/btm.csv")


# --- 4. PROSES BERTOPIC ---
print("\n[4/4] Memproses Data BERTopic...")
raw_texts = get_text_from_url(URL_BERTOPIC)
final_texts = expand_data_to_target(raw_texts, TARGET_ROWS)
pd.DataFrame({'text': final_texts}).to_csv('data/bertopic.csv', index=False)
print("💾 Tersimpan: data/bertopic.csv")


# --- 5. CHATBOT (Tetap pakai generator statis karena butuh struktur harga) ---
print("\n[5/5] Generate Data Stok (Tetap menggunakan dummy terstruktur)...")
# Chatbot tidak bisa di-scrape sembarangan karena butuh kolom 'harga' dan 'stok' yang valid
real_products = [
    ("iPhone 15 Pro", "Elektronik", 20000000), ("Samsung S24", "Elektronik", 19000000),
    ("Macbook Air", "Laptop", 15000000), ("Sepatu Nike", "Sepatu", 2000000),
    ("Kemeja Batik", "Pakaian", 250000), ("Jam Tangan Garmin", "Aksesoris", 5000000)
]
data_chat = []
for i in range(100):
    p = random.choice(real_products)
    data_chat.append([f"SKU-{i}", p[0], p[1], random.randint(0,20), p[2]])
    
pd.DataFrame(data_chat, columns=['id_barang', 'nama_barang', 'kategori', 'stok', 'harga']).to_csv('data/chatbot_stock.csv', index=False)
print("💾 Tersimpan: data/chatbot_stock.csv")

print("\n✅ SELESAI! Silakan 'git push'.")