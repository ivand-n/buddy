import pandas as pd
from supabase import create_client, Client
from google import genai
from google.genai import types
import numpy as np
import os
from dotenv import load_dotenv

# 1. KONFIGURASI API
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inisialisasi Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
client = genai.Client()

def get_embedding(text):
    """Fungsi untuk mengubah teks menjadi vektor menggunakan Gemini"""
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=1536),
    )
    print(result.embeddings[0].values)
    return result.embeddings[0].values

# 2. LOAD DATA DARI KAGGLE (CSV)
df = pd.read_csv('cleaned.csv') # Sesuaikan nama file Anda

print(f"Mulai memproses {len(df)} data...")

# 3. LOOPING UNTUK EMBEDDING & UPLOAD
for index, row in df.iterrows():
    # Buat teks gabungan sebagai konteks untuk AI
    text_context = f"Transaksi pada {row['Date']} jam {row['Time']} membeli {row['Item']} dengan harga {row['Price']} sebanyak {row['Quantity']} dengan total {row['Total']} dengan metode pembayaran {row['Payment Method']}. Kepuasan pelanggan: {row['Customer Satisfaction']}. Cuaca saat itu: {row['Weather']} . Penawaran spesial: {row['Special Offers']}."
    
    try:
        # Generate Vector
        vector = get_embedding(text_context)
        
        # Data yang akan diinsert ke Supabase
        data_to_insert = {
            "date": row['Date'],
            "time": row['Time'],
            "item": row['Item'],
            "price": row['Price'],
            "quantity": row['Quantity'],
            "total": row['Total'],
            "payment": row['Payment Method'],
            "satisfaction": row['Customer Satisfaction'],
            "weather": row['Weather'],
            "spesial": row['Special Offers'],
            "embedding": vector # Kolom vector(768) di Supabase
        }
        
        # Upload ke tabel 'transaksi'
        supabase.table("transaksi").insert(data_to_insert).execute()
        
        print(f"[{index+1}/{len(df)}] Berhasil upload")
        
    except Exception as e:
        print(f"Error pada baris {index}: {e}")

print("Proses Selesai!")