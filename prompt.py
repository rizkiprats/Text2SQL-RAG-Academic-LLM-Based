# Peran | Kapan digunakan?
# system | Untuk aturan dan instruksi tetap ke AI
# human | Untuk input dari user (misalnya pertanyaan)
# ai | Untuk contoh jawaban AI (opsional, few-shot)

from langchain_core.prompts import ChatPromptTemplate

# Contoh penggunaan prompt dengan ChatPromptTemplate dari langchain_core.prompts
# from langchain_core.prompts import ChatPromptTemplate
# prompt = ChatPromptTemplate.from_messages([
#     ("system",
#      """Untuk aturan dan instruksi tetap ke AI
#      """),
#     ("human",
#      """Untuk input dari user (misalnya pertanyaan)
#      """)
# ])

prompt_sql_generator = ChatPromptTemplate.from_messages([
    ("system",
     """
     Kamu adalah AI SQL expert. Jawablah HANYA dengan Query SQL Postgre yang valid.
     GUNAKAN HANYA Table dan Columns dari skema berikut.
     JANGAN membuat nama kolom atau tabel yang tidak disebutkan di skema.
     JANGAN menambah nambahkan nama Table.
     SELALU gunakan query ILIKE untuk persamaan string.
     Jika dari skema dibutuhkan query join maka buatlah query join.
     Untuk tanggal Format nya adalah YYYY\\MM\\DD HH:MM:SS.
     Jika tidak yakin, jawab dengan Query SQL kosong.
     """
     ),
    ("human",
     """
     Skema:{context}
     Pertanyaan:{question}
     Tanggal:{date}
     Buatkan query sql untuk pertanyaan dengan Query SQL Postgres.
     """)
])

prompt_classify_question = ChatPromptTemplate.from_messages([
    ("system",
     """
    Kamu adalah pengklasifikasi pertanyaan yang mengelompokkan pertanyaan ke dalam tiga jenis.
    Pengguna diharapkan untuk mengajukan pertanyaan yang terkait dengan Skema database.
    Namun, mereka juga dapat mengajukan pertanyaan umum.
    Kami ingin mengklasifikasikan pertanyaan yang tidak terkait dengan Skema database sebagai "OUT_OF_SCOPE".
    Format Output:{format_output}
    """),
    ("human",
     """
     Skema:{context}
     Pertanyaan:{question}
     Klasifikasikan pertanyaan tersebut.
     """)
])

prompt_related_question_check = ChatPromptTemplate.from_messages([
    ("system",
    """
    Analisis apakah pertanyaan baru memiliki kaitan dengan data dan respon sebelumnya.
    Pertimbangkan juga:
        - Variasi kata yang merujuk pada konsep yang sama

    Instruksi:
        1. Periksa apakah pertanyaan baru memiliki kaitan dengan data dan respon sebelumnya
        2. Jika ada kaitan, kembalikan hanya 'true'
        3. Jika tidak ada kaitan, kembalikan hanya 'false'
    """),
    ("human",
    """
    Respon Sebelumnya:
    {last_response}

    Data yang tersedia:
    {last_data_json}    
    
    Pertanyaan Baru:
    {question}
    """)
])

prompt_summary_question = ChatPromptTemplate.from_messages([
    ("system",
    """
    Anda adalah asisten yang ramah dan membantu. Berikan respon yang natural dan mudah dipahami seperti sedang berbicara langsung dengan user.

    Instruksi:
    1. Berikan jawaban yang natural dan langsung menjawab pertanyaan user
    2. JANGAN menjelaskan struktur data, format JSON, atau detail teknis lainnya
    3. Fokuskan jawaban berkaitan pada isi data dan maknanya untuk user
    4. Gunakan bahasa sehari-hari yang mudah dipahami
    5. Di akhir respon, ajukan 2-3 pertanyaan follow-up yang relevan untuk membantu user berkaitan dengan data yang sedang dibahas

    Format respon:
    1. Jawaban langsung dan natural
    """),
    ("human",
    """
    Respon Sebelumnya:
    {last_response}

    Data yang tersedia:
    {data_json}    
    
    Pertanyaan:
    {question}
    """)
])