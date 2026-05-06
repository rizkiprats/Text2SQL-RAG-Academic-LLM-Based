from constant import (JWT_SECRET_KEY)
from flask import Flask, render_template, jsonify, request, session
from users import User

import re
import json

from flask_cors import CORS
import jwt
import datetime
from functools import wraps
from dotenv import load_dotenv

from lib import Text2SQLRAG, TextRAG
from cache_manager import SQLResponseCache
from general_chat import chat_general_context
from database_chat import chat_database_context
from document_files_chat import chat_document_files_context

load_dotenv()

app = Flask(__name__)
# Mengizinkan semua origin, atau sesuaikan: CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
CORS(app)

app.config['SECRET_KEY'] = JWT_SECRET_KEY

# Initialize RAG instance
text2sql = Text2SQLRAG()
text = TextRAG()


@app.route('/')
def home():
    return render_template('index.html')

# Decorator untuk validasi token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Ambil token dari header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token tidak ditemukan!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
            current_role = data['role']
            current_id_user = data['id_user']

            session['current_user'] = current_user
            session['current_role'] = current_role
            session['current_id_user'] = current_id_user
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token tidak valid!'}), 401

        return f(*args, **kwargs)

    return decorated

# Endpoint login
@app.route('/login', methods=['POST'])
def login():
    auth = request.json

    if not auth or not auth.get('username') or not auth.get('password') or not auth.get('role'):
        return jsonify({'message': 'Username, password dan role diperlukan!'}), 400

    username = auth['username']
    password = auth['password']
    role = auth['role']

    if role == "Student":
        try:
            user = User(username, role, password)
            personal_data = user.get_personal_data()
            if personal_data:
                personal_data_json = json.loads(personal_data)
                id_user = personal_data_json[0]["id"]

                if id_user != password:
                    return jsonify({'message': 'Login gagal! Password Salah'}), 401

                token = jwt.encode({
                    'username': username,
                    'role': role,
                    'id_user': id_user,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                }, app.config['SECRET_KEY'], algorithm="HS256")

        except Exception as e:
            return jsonify({'message': 'Login gagal! User Tidak Ditemukan'}), 401
    elif role == "Instructor":
        try:
            user = User(username, role, password)
            personal_data = user.get_personal_data()
            if personal_data:
                personal_data_json = json.loads(personal_data)
                id_user = personal_data_json[0]["id"]

                if id_user != password:
                    return jsonify({'message': 'Login gagal! Password Salah'}), 401

                token = jwt.encode({
                    'username': username,
                    'role': role,
                    'id_user': id_user,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                }, app.config['SECRET_KEY'], algorithm="HS256")

        except Exception as e:
            return jsonify({'message': 'Login gagal! User Tidak Ditemukan'}), 401
    else:
        return jsonify({'message': 'Login gagal! Role tidak valid!'}), 400

    return jsonify({'token': token})


@app.route('/chat', methods=['POST'])
# @token_required
def chat():
    data = request.get_json()
    chat_message = data.get('message', '')

    if session.get('current_user'):
        ROLE = session.get('current_role')
        NAME = session.get('current_user')
        ID = session.get('current_id_user')
    else:
        # ROLE = "public"
        # NAME = "Schrefl"
        # ID = "0"

        # ROLE = "Instructor"
        # NAME = "McKinnon"
        # ID = "63395"

        ROLE = "Student"
        NAME = "Schrefl"
        ID = "24746"

    role = ROLE
    name = NAME
    id = ID

    print("role : ", role)
    print("name : ", name)
    print("id : ", id)
    
    user = User(name, role, id)
    
    id_user = "public"
    
    personal_data = user.get_personal_data()
    print("personal_data : ", personal_data)
    
    if personal_data:
        personal_data_json = json.loads(personal_data)
        
        name_from_db = personal_data_json[0]["name"]
        id_user = personal_data_json[0]["id"]
        print("id_user : ", id_user)

        cacheManager = SQLResponseCache(cache_file=f"{id_user}_{name_from_db}_cache.json")
        cacheManager.set(chat_message, {'answer_summary': "", 'answer_data': None})

    else:
        cacheManager = SQLResponseCache(cache_file=f"{role}_{name}_cache.json")
        cacheManager.set(chat_message, {'answer_summary': "", 'answer_data': None})

    cache = cacheManager.get(chat_message)
    last_response = cache["answer_summary"] if cache else ""
    last_data_json = cache["answer_data"] if cache else None
    
    print("cache : ", cache)
    print("last_response : ", last_response)
    print("last_data_json : ", last_data_json)

    def chat_logic(last_response, last_data_json, chat_message, id_user, personal_data, role):
        current_date = datetime.datetime.now()
        current_date_str = current_date.strftime("%Y-%m-%d")
        print("current_date_str : ", current_date_str)

        if not chat_message:
            return {'error': 'No message provided'}, 400

        response_classify = text2sql.run_classify_question(chat_message, text.retriever)
        print("response_classify : ", response_classify)
        
        query_type = json.loads(response_classify)["queryType"]
        print("query_type : ", query_type)

        if (query_type == "GENERAL_QUESTION"):
            response_data, response_code = chat_general_context(text, last_response, last_data_json, chat_message)
        elif (query_type == "DATA_QUESTION"):
            response_data, response_code = chat_database_context(text2sql, text, last_response, last_data_json, chat_message)
        else:
            response_data, response_code = chat_document_files_context(text, last_response, last_data_json, chat_message)
        
        return response_data, response_code

    TIMEOUT_SECONDS = 60  # Set timeout in seconds

    import concurrent

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(chat_logic, last_response, last_data_json, chat_message, id_user, personal_data, role)
        
        try:
            response_data, response_code = future.result(timeout=TIMEOUT_SECONDS)
            response_answer = response_data.get('answer_summary', "")
            dataframe_json = json.dumps(response_data.get('dataframe_json', None))

            cacheManager.set(chat_message, {'answer_summary': response_answer, 'answer_data': dataframe_json})
            
            return jsonify(response_data), response_code
        except concurrent.futures.TimeoutError:
            return jsonify({'error': 'Request timed out'}), 504
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)