# Text2SQL-RAG-Academic-LLM-Based

A Flask-based chatbot application that combines Text-to-SQL generation, Retrieval-Augmented Generation (RAG), and document search to answer academic questions across:

- PostgreSQL database queries via natural language
- Document file search from `document_files/`
- General web context via Google search

The app uses a local Ollama LLM for SQL generation and summary responses, plus HuggingFace embeddings and Chroma vector indexing.

## Features

- Natural language to SQL translation using database schema retrieval
- Question classification into:
  - `DATA_QUESTION` for database queries
  - `GENERAL_QUESTION` for web/contextual answers
  - `OUT_OF_SCOPE` for document-based responses
- Local chat UI served from `templates/index.html`
- Query caching per user in `history_chat_users/`
- File-based RAG for `pdf`, `docx`, and Excel documents in `document_files/`
- JWT-based login flow for `Student` and `Instructor`

## Project Structure

- `app_flask.py` - Flask application, API endpoints, session/token handling, chat orchestration
- `lib.py` - Core RAG logic and Text2SQL model integration
- `prompt.py` - Prompt templates for SQL generation, classification, and summarization
- `cache_manager.py` - Question/response cache management using TF-IDF similarity
- `database_chat.py` - Database query chat handler
- `document_files_chat.py` - Document search chat handler
- `general_chat.py` - General web/search chat handler
- `users.py` - User validation and personal data lookup
- `utils.py` - PostgreSQL utility helpers and JSON/DataFrame conversions
- `constant.py` - Environment-based configuration values
- `document_files/` - Input documents for RAG
- `history_chat_users/` - Cached chat histories per user
- `templates/index.html` - Frontend chat UI

## Requirements

Install the project dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Environment Setup

The app loads settings from `.env` and expects the following keys:

- `FLASK_APP`
- `FLASK_ENV`
- `FLASK_RUN_HOST`
- `FLASK_RUN_PORT`
- `FLASK_DEBUG`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `SQL_LLM_MODEL`
- `GENERAL_LLM_MODEL`
- `EMBEDDING_MODEL`
- `EMBEDDING_MODEL_SQL`
- `JWT_SECRET_KEY`

Example `.env` values are already defined in the repository.

## Running the App

Start the Flask server with:

```bash
python app_flask.py
```

Then open:

```text
http://localhost:5000
```

## Usage

- Access the chat UI in the browser
- Enter a question in natural language
- The backend classifies the request and routes it to:
  - `general_chat` for general info searches
  - `database_chat` for SQL-based answers
  - `document_files_chat` for document-based QA

## Authentication

The app includes a login endpoint at `/login` expecting JSON with:

```json
{
  "username": "...",
  "password": "...",
  "role": "Student" | "Instructor"
}
```

A JWT token is returned on successful login.

> Note: In the current front-end demo, `/chat` is used without authentication.

## Important Notes

- The application depends on a local Ollama instance at `http://localhost:11434`
- PostgreSQL must be available with the configured database and schema
- Document ingestion supports `pdf`, `docx`, `xlsx`, and `xls`
- Cached responses are stored in `history_chat_users/`

## Customization

- Add documents to `document_files/` for RAG search
- Update environment variables in `.env` for your PostgreSQL and model settings
- Modify `prompt.py` to refine SQL generation and summarization behavior

## Troubleshooting

- Ensure `POSTGRES_*` values are correct and PostgreSQL is running
- Confirm Ollama is running locally with the configured model names
- If embeddings fail, verify HuggingFace models are accessible
- Check logs in the terminal for prompt/debug output
