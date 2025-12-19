from google import genai
from google.genai import types
from supabase import create_client
import os
from dotenv import load_dotenv

#setup
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = genai.Client()

def embedtext(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=1536)
    )
    return result.embeddings[0].values

def buddy(question):
    question_vector = embedtext(question)

    response = supabase.rpc('match_transaksi', {
        'query_embedding': question_vector,
        'match_threshold': 0.4,
        'match_count': 10
    }).execute()

    context = response.data

    text = "\n".join([f"Transaksi pada {row['date']} jam {row['waktu']} membeli {row['item']} dengan harga {row['price']} sebanyak {row['quantity']} dengan total {row['total']} dengan metode pembayaran {row['payment']}. Kepuasan pelanggan: {row['satisfaction']}. Cuaca saat itu: {row['weather']} . Penawaran spesial: {row['spesial']}." for row in context])

    prompt = f"""
    Anda Adalah asisten keuangan pribadi bernama buddy. gunakan data berikut untuk menjawab pertanyaan user.
    jika data tidak ditemukan, katakan anda tidak mengetahui jangan mengarang jawaban.

    DATA TRANSAKSI USER :
    {text}

    PERTANYAAN USER :
    {question}

    JAWABAN ANDA :
    """

    gemini_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return gemini_response.text

# main
print("Buddy siap membantu keuangan kamu (ketik 'keluar' untuk berhenti)!")
while True:
    user_input = input("\nanda : ")
    if user_input.lower() == 'keluar':
        print("Terima kasih telah menggunakan Buddy. Sampai jumpa!")
        break

    answer = buddy(user_input)
    print(f"\nbuddy : {answer}")