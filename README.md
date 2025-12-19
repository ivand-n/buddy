# 💰 Buddy AI: Financial Assistant (Gojek Ecosystem)

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Supabase](https://img.shields.io/badge/Database-Supabase%20(pgvector)-3ECF8E.svg)](https://supabase.com/)
[![Gemini](https://img.shields.io/badge/AI-Gemini%202.5--Flash-blueviolet.svg)](https://deepmind.google/technologies/gemini/)

**Buddy AI** adalah asisten finansial cerdas yang dirancang khusus untuk memantau dan menganalisis transaksi. Dengan menggunakan teknik **RAG (Retrieval-Augmented Generation)**, asisten ini tidak hanya berbicara, tetapi "memahami" riwayat transaksi Anda secara presisi.

---

## 🚀 Fitur Utama

- **Natural Language Query:** Tanya riwayat pengeluaran Anda dengan bahasa sehari-hari (Contoh: "Berapa kali saya jajan kopi minggu lalu?").
- **Smart Insight & Summary:** Mendapatkan ringkasan pengeluaran bulanan dan saran penghematan otomatis.
- **Context-Aware RAG:** Menggunakan pencarian vektor untuk mengambil data transaksi yang paling relevan sebelum memberikan jawaban.
- **Merchant Analysis:** Memahami kategori merchant (GoFood, GoRide, GoSend) secara mendalam.

## 🧠 Arsitektur RAG (Cara Kerja)

Proyek ini tidak hanya mengandalkan ingatan model AI, melainkan menghubungkan **Gemini 2.5-Flash** dengan database transaksi pribadi melalui alur berikut:



1. **Embedding:** Mengubah data transaksi Kaggle menjadi vektor menggunakan `models/embedding-001`.
2. **Storage:** Menyimpan vektor ke dalam **Supabase (PostgreSQL)** dengan ekstensi `pgvector`.
3. **Retrieval:** Mencari transaksi paling relevan berdasarkan kemiripan kosinus (cosine similarity) saat user bertanya.
4. **Generation:** Mengirimkan data tersebut ke Gemini untuk dirangkum menjadi jawaban natural.

## 🛠️ Tech Stack

- **Language:** Python 3.13
- **AI Model:** Gemini 2.5-Flash (via Google Generative AI SDK)
- **Vector Database:** Supabase + `pgvector`
- **Orchestration:** RAG Logic with Python
- **Frontend:** Streamlit
