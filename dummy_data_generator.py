import pandas as pd
import random
import os

# Buat folder data jika belum ada
if not os.path.exists('data'):
    os.makedirs('data')

NUM_DATA = 10000  # Total data per file

print("🚀 Sedang men-generate 10.000+ data dummy... Mohon tunggu sebentar.")

# ==========================================
# 1. DATA SENTIMENT (10.000 Baris)
# ==========================================
subjects = ["Barang ini", "Paketnya", "Produknya", "Kualitasnya", "Pelayanannya", "Pengirimannya", "Bahannya"]
adverbs = ["sangat", "cukup", "lumayan", "agak", "benar-benar", "terlalu"]
pos_adj = ["bagus", "memuaskan", "keren", "oke", "cepat", "rapi", "mantap", "halus", "original"]
neg_adj = ["jelek", "mengecewakan", "lambat", "rusak", "palsu", "kasar", "buruk", "penyok"]

data_sentimen = []
for _ in range(NUM_DATA):
    if random.random() > 0.5:
        # Generate Positif
        text = f"{random.choice(subjects)} {random.choice(adverbs)} {random.choice(pos_adj)}."
        label = "Positif"
    else:
        # Generate Negatif
        text = f"{random.choice(subjects)} {random.choice(adverbs)} {random.choice(neg_adj)}."
        label = "Negatif"
    data_sentimen.append([text, label])

df_sentimen = pd.DataFrame(data_sentimen, columns=['text', 'label_manual'])
df_sentimen.to_csv('data/sentiment.csv', index=False)
print("✅ data/sentiment.csv dibuat (10k rows)")


# ==========================================
# 2. DATA LDA - TEKS PANJANG/ARTIKEL (10.000 Baris)
# ==========================================
# Kita buat kalimat berdasarkan topik agar LDA bisa memisahkan
topik_politik = ["Pemerintah membahas undang-undang baru.", "Pemilu akan diadakan tahun depan.", "Partai politik berkampanye.", "Kebijakan fiskal negara diperketat.", "DPR mengadakan rapat paripurna."]
topik_bola = ["Timnas menang telak melawan musuh.", "Striker mencetak gol indah.", "Pelatih merombak strategi permainan.", "Pertandingan berlangsung sengit di stadion.", "Liga champion memasuki babak final."]
topik_teknologi = ["Smartphone terbaru dirilis dengan kamera canggih.", "AI semakin berkembang pesat.", "Laptop gaming ini memiliki spesifikasi tinggi.", "Jaringan 5G mulai merata.", "Startup teknologi mendapatkan pendanaan."]

data_lda = []
for _ in range(NUM_DATA):
    kategori = random.choice(['politik', 'bola', 'teknologi'])
    if kategori == 'politik':
        base = random.sample(topik_politik, 2)
    elif kategori == 'bola':
        base = random.sample(topik_bola, 2)
    else:
        base = random.sample(topik_teknologi, 2)
    
    # Gabungkan jadi "paragraf" pendek
    text = " ".join(base) + " Berita ini sedang hangat diperbincangkan."
    data_lda.append([text])

df_lda = pd.DataFrame(data_lda, columns=['text'])
df_lda.to_csv('data/lda.csv', index=False)
print("✅ data/lda.csv dibuat (10k rows)")


# ==========================================
# 3. DATA BTM - SHORT TEXT/SOSMED (10.000 Baris)
# ==========================================
lokasi = ["Sudirman", "Bundaran HI", "Tol Dalam Kota", "Stasiun Manggarai", "Bekasi", "Tangerang"]
aktivitas = ["Macet parah", "Hujan deras", "Lagi ngopi", "Nunggu kereta", "Pulang kerja", "Lapar banget"]
hashtag = ["#jktinfo", "#macet", "#kuliner", "#curhat", "#info"]

data_btm = []
for _ in range(NUM_DATA):
    text = f"{random.choice(aktivitas)} di {random.choice(lokasi)} nih. {random.choice(hashtag)}"
    data_btm.append([text])

df_btm = pd.DataFrame(data_btm, columns=['text'])
df_btm.to_csv('data/btm.csv', index=False)
print("✅ data/btm.csv dibuat (10k rows)")


# ==========================================
# 4. DATA BERTopic - KELUHAN TEKNIS (10.000 Baris)
# ==========================================
device = ["Laptop", "HP", "Modem", "Router", "Aplikasi", "Akun"]
masalah = ["tidak bisa nyala", "mati total", "lemot banget", "sering crash", "lupa password", "kena virus", "layar blank"]
solusi = ["Gimana solusinya?", "Tolong bantuannya.", "Ada yang tau cara fix?", "Harus bawa ke service center?", "Mohon pencerahan."]

data_bertopic = []
for _ in range(NUM_DATA):
    text = f"{random.choice(device)} saya {random.choice(masalah)}. {random.choice(solusi)}"
    data_bertopic.append([text])

df_bertopic = pd.DataFrame(data_bertopic, columns=['text'])
df_bertopic.to_csv('data/bertopic.csv', index=False)
print("✅ data/bertopic.csv dibuat (10k rows)")


# ==========================================
# 5. DATA CHATBOT STOK (Kecil - 50 Baris)
# ==========================================
# Chatbot butuh data akurat, tidak boleh random gibberish
barang = [
    ("iPhone 13", "Elektronik", 10000000), ("iPhone 14", "Elektronik", 12000000), ("iPhone 15 Pro", "Elektronik", 20000000),
    ("Samsung S23", "Elektronik", 11000000), ("Samsung S24 Ultra", "Elektronik", 19000000), ("Xiaomi 13", "Elektronik", 8000000),
    ("Macbook Air M1", "Laptop", 13000000), ("Macbook Pro M2", "Laptop", 22000000), ("Asus ROG", "Laptop", 25000000),
    ("Kemeja Flanel", "Pakaian", 150000), ("Kaos Polos", "Pakaian", 50000), ("Jaket Bomber", "Pakaian", 250000),
    ("Celana Jeans", "Pakaian", 200000), ("Celana Chino", "Pakaian", 180000), ("Hoodie Polos", "Pakaian", 120000),
    ("Sepatu Nike", "Sepatu", 1500000), ("Sepatu Adidas", "Sepatu", 1300000), ("Sepatu Vans", "Sepatu", 800000),
    ("Sandal Jepit", "Sepatu", 15000), ("Sandal Gunung", "Sepatu", 150000)
]

data_chatbot = []
for item in barang:
    # Buat variasi stok random tapi masuk akal
    nama, kat, harga = item
    stok = random.randint(0, 50) # Stok antara 0 sampai 50
    data_chatbot.append([f"BRG-{random.randint(100,999)}", nama, kat, stok, harga])

# Tambahkan duplikat/variasi sedikit biar genap 50 baris
while len(data_chatbot) < 50:
    item = random.choice(barang)
    nama, kat, harga = item
    stok = random.randint(0, 50)
    data_chatbot.append([f"BRG-{random.randint(100,999)}", nama, kat, stok, harga])

df_chat = pd.DataFrame(data_chatbot, columns=['id_barang', 'nama_barang', 'kategori', 'stok', 'harga'])
df_chat.to_csv('data/chatbot_stock.csv', index=False)
print("✅ data/chatbot_stock.csv dibuat (50 rows)")

print("\n🎉 SELESAI! Semua dataset telah dibuat di folder 'data/'. Silakan git push.")