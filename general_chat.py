import json
from lib import TextRAG
import requests
from bs4 import BeautifulSoup
from googlesearch import search

from utils import json_to_dataframe

def get_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # cek status code
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ambil semua teks dari paragraf
        paragraphs = soup.find_all('p')
        text = '\n'.join([p.get_text() for p in paragraphs])
        return text[:3000]  # batas karakter untuk prompt LLM
    except Exception as e:
        return f"[ERROR] Gagal mengambil dari {url}: {e}"

def chat_general_context(text :TextRAG, last_response, last_data_json, current_question):
    # Initialize response data
    response_data = {
        # 'sql_query': sql_query,
        # 'reasoning': reasoning,
        'dataframe': None,
        'answer_summary': '',
        'dataframe_json': None
    }

    if last_response is not None or last_data_json is not None:
        is_related = text.run_related_context_check(current_question, last_response, last_data_json)
        print("is_related: ", is_related)

        if is_related:
            try:
                response = text.run_summary_context(current_question, last_response, last_data_json)
                print("response summary general chat related: ", response)
                df = json_to_dataframe(last_data_json)

                response_data['answer_summary'] = response
                response_data['dataframe_json'] = json.loads(last_data_json)
                response_data['dataframe'] = df

            except Exception as e:
                print (f"Error processing request: {str(e)}")
                return {'error': 'Internal server error'}, 500
        else:
            try:
                urls = []
                for result in search(current_question, num_results=5):
                    print("result google search", result)
                    urls.append(result)
                print("urls : ", urls)
                
                all_contents = []
                for url in urls:
                    content = get_text_from_url(url)
                    all_contents.append(content)
                print("all_contents : ", all_contents)

                response = text.run_summary_context(current_question, "", all_contents)
                print("response summary general chat not related: ", response)

                response_data['answer_summary'] = response
                response_data['dataframe_json'] = None
                response_data['dataframe'] = None

            except Exception as e:
                print (f"Error processing request: {str(e)}")
                return {'error': 'Internal server error'}, 500
    else:
        try:
            urls = []
            for result in search(current_question, num_results=5):
                print("result google search", result)
                urls.append(result)
            print("urls : ", urls)
            
            all_contents = []
            for url in urls:
                content = get_text_from_url(url)
                all_contents.append(content)
            print("all_contents : ", all_contents)
            
            response = text.run_summary_context(current_question, "", all_contents)
            print("response summary general chat: ", response)

            response_data['answer_summary'] = response
            response_data['dataframe_json'] = None
            response_data['dataframe'] = None
            
        except Exception as e:
            print (f"Error processing request: {str(e)}")
            return {'error': 'Internal server error'}, 500

    return response_data, 200