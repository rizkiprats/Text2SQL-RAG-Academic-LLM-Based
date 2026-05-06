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

    Instruksi:
    1. GUNAKAN HANYA Table dan Columns dari skema berikut.
    2. JANGAN membuat nama kolom atau tabel yang tidak disebutkan di skema.
    3. JANGAN menambah nambahkan nama Table.
    4. SELALU gunakan query ILIKE untuk persamaan string.
    5. Jika dari skema dibutuhkan query join maka buatlah query join.
    6. Untuk tanggal Format nya adalah YYYY\\MM\\DD HH:MM:SS.
    7. Jika tidak yakin, jawab dengan Query SQL kosong.

    Skema:
    {context}
    
    Tanggal:
    {date}
    """
    ),
    ("human",
    """
    Pertanyaan:
    {question}
    
    Buatkan query sql untuk pertanyaan dengan Query SQL Postgres.
    """)
])

prompt_classify_question = ChatPromptTemplate.from_messages([
    ("system",
    """
    Kamu adalah pengklasifikasi pertanyaan yang mengelompokkan pertanyaan ke dalam tiga jenis.

    Klasifikasi Pertanyaan:
    1. DATA_QUESTION
    2. DOCUMENT_QUESTION
    3. GENERAL_QUESTION

    Data pengetahuan untuk klasifikasi:
    Skema:
    {sql_context}
    
    File Dokumen:
    {document_files_context}

    Instruksi Klasifikasi: 
    1. Pertanyaan yang terkait dengan Skema database akan dikategorikan sebagai DATA_QUESTION.
    2. Pertanyaan yang terkait dengan File Dokumen akan dikategorikan sebagai DOCUMENT_QUESTION.
    3. Pertanyaan yang tidak terkait dengan Skema database atau File Dokumen dianggap sebagai GENERAL_QUESTION.

    Format response:
    1. Berikan jawaban dalam bentuk JSON dengan formart {format_output}
    """),
    ("human",
    """
    Pertanyaan:
    {question}
    
    Klasifikasikan pertanyaan tersebut.
    """)
])

prompt_related_question_check = ChatPromptTemplate.from_messages([
    ("system",
    """
    Analisis apakah pertanyaan baru memiliki kaitan dengan data dan respon sebelumnya.

    Respon Sebelumnya:
    {last_response}

    Data yang tersedia:
    {last_data_json}
    
    Pertimbangkan juga:
    1. Variasi kata yang merujuk pada konsep yang sama

    Instruksi:
    1. Periksa apakah pertanyaan baru memiliki kaitan dengan data dan respon sebelumnya
    2. Jika ada kaitan, kembalikan hanya 'true'
    3. Jika tidak ada kaitan, kembalikan hanya 'false'
    """),
    ("human",
    """
    Pertanyaan Baru:
    {question}
    """)
])

prompt_summary_question = ChatPromptTemplate.from_messages([
    ("system",
    """
    Anda adalah asisten yang ramah dan membantu. Berikan respon yang natural dan mudah dipahami seperti sedang berbicara langsung dengan user.

    Respon Sebelumnya:
    {last_response}

    Data yang tersedia:
    {data_json}    

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
    Pertanyaan:
    {question}
    """)
])