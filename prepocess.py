import pandas as pd
import os
import re

# 1. Masukkan Teks Mentah Kamu di Sini
# (Gunakan triple quotes """ agar bisa paste teks panjang beserta enter-enternya)
raw_text = pd.read_csv("data/dataset_pidato_UN.csv")


# 2. Proses Pembersihan & Pemecahan (Chunking)
def process_speech(text):
    # A. Pecah berdasarkan baris baru (Enter)
    lines = text.split('\n')
    
    clean_data = []
    
    for line in lines:
        line = line.strip() # Hapus spasi di awal/akhir
        
        # B. Filter Baris Kosong
        if not line:
            continue
            
        # C. Filter Judul (Opsional: Hapus baris yang mengandung 'PIDATO' atau tanggal)
        if "PIDATO" in line.upper() and "2025" in line:
            print(f"⚠️ Membuang Judul: {line}")
            continue
            
        # D. Bersihkan tanda kutip berlebih (misal """Semua manusia...)
        line = line.replace('"""', '"').replace('""', '"')
        
        # E. Simpan paragraf yang valid
        # Kita anggap valid jika panjangnya lebih dari 10 karakter (biar bukan sampah)
        if len(line) > 10:
            clean_data.append(line)
            
    return clean_data

# Jalankan Proses
chunks = process_speech(raw_text)

# 3. Simpan ke DataFrame & CSV
df_speech = pd.DataFrame(chunks, columns=['text'])

# Tambahkan ID agar terlihat rapi (Opsional)
df_speech['id_paragraf'] = range(1, len(df_speech) + 1)

# Buat folder data jika belum ada
if not os.path.exists('data'):
    os.makedirs('data')

# Save
output_path = 'data/bertopic.csv'
df_speech.to_csv(output_path, index=False)

print(f"\n✅ Berhasil! Teks pidato telah dipecah menjadi {len(df_speech)} baris data.")
print(f"📂 File tersimpan di: {output_path}")
print("\nPreview Data untuk BERTopic:")
print(df_speech[['id_paragraf', 'text']].head())