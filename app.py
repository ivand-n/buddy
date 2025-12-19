import streamlit as st
from google import genai
from google.genai import types
from supabase import create_client
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Buddy - Asisten keuangan Pribadi", page_icon="💰", layout="wide")

#setup
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = genai.Client()

with st.sidebar:
    if st.button("Hapus riwayat chat"):
        st.session_state.messages = []

def embedtext(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=1536)
    )
    return result.embeddings[0].values

st.title("💰 Buddy - Asisten Keuangan Pribadi")
st.markdown("Tanyakan apa saja tentang riwayat transaksi anda")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Contoh : Pembelian terbanyak saya apa saja ya?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buddy lagi mikir gais.."):
            try:
                q_vector = embedtext(prompt)
                res = supabase.rpc('match_transaksi', {
                    'query_embedding': q_vector,
                    'match_threshold': 0.4,
                    'match_count': 50
                }).execute()

                context = res.data

                text = "\n".join([f"Transaksi pada {row['date']} jam {row['waktu']} membeli {row['item']} dengan harga {row['price']} sebanyak {row['quantity']} dengan total {row['total']} dengan metode pembayaran {row['payment']}. Kepuasan pelanggan: {row['satisfaction']}. Cuaca saat itu: {row['weather']} . Penawaran spesial: {row['spesial']}." for row in context])
                
                prompt_full = f"""
                Anda Adalah asisten keuangan pribadi bernama buddy. gunakan data berikut untuk menjawab pertanyaan user.
                jika data tidak ditemukan, katakan anda tidak mengetahui jangan mengarang jawaban.

                DATA TRANSAKSI USER :
                {text}

                PERTANYAAN USER :
                {prompt}

                JAWABAN ANDA :
                """

                gemini_response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_full,
                )

                st.markdown(gemini_response.text)
                st.session_state.messages.append({"role": "assistant", "content": gemini_response.text})
            
            except Exception as e:
                st.markdown("Maaf, terjadi kesalahan saat memproses permintaan Anda.")
