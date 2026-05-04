import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),    
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

MODELS = {
    "sql_llm_model": os.getenv("SQL_LLM_MODEL"),
    "general_llm_model": os.getenv("GENERAL_LLM_MODEL"),
    "embedding_model": os.getenv("EMBEDDING_MODEL"),
    "embedding_model_sql": os.getenv("EMBEDDING_MODEL_SQL")
}

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")