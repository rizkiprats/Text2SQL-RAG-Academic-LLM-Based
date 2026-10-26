import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),    
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}

MODELS = {
    "embedding_model": os.getenv("EMBEDDING_MODEL"),
    "embedding_model_sql": os.getenv("EMBEDDING_MODEL_SQL"),
    
    "ollama_server_url": os.getenv("OLLAMA_SERVER_URL"),
    "sql_llm_model": os.getenv("SQL_LLM_MODEL"),
    "general_llm_model": os.getenv("GENERAL_LLM_MODEL"),
    
    "use_vllm": os.getenv("USE_VLLM", "False").lower() == "true",
    "vllm_server_url": os.getenv("VLLM_SERVER_URL")
}

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")