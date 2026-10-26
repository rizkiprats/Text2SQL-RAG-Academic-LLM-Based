from lib import TextRAG
from utils import json_to_dataframe
import json

def chat_document_files_context(text :TextRAG, last_response, last_data_json, current_question):
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
        print("is_related : ", is_related)

        if is_related:
            try:
                response = text.run_summary_context(current_question, last_response, last_data_json)
                print("response summary document files chat related: ", response)
                df = json_to_dataframe(last_data_json)

                response_data['answer_summary'] = response
                response_data['dataframe_json'] = json.loads(last_data_json)
                response_data['dataframe'] = df

            except Exception as e:
                print (f"Error processing request: {str(e)}")
                return {'error': 'Internal server error'}, 500
        else:
            try:
                # Document-based response
                if text.retriever:
                    docs = text.retriever.invoke(current_question)
                    context_docs = "\n\n".join(
                        [doc.page_content for doc in docs])
                else:
                    context_docs = ""
                response = text.run_summary_context(current_question, "", context_docs)
                print("response summary document files chat not related: ", response)

                response_data['answer_summary'] = response
                response_data['dataframe_json'] = None
                response_data['dataframe'] = None

            except Exception as e:
                print(f"Error processing request: {str(e)}")
                return {'error': 'Internal server error'}, 500

    else:
        try:
            # Document-based response
            if text.retriever:
                docs = text.retriever.invoke(current_question)
                context_docs = "\n\n".join(
                    [doc.page_content for doc in docs])
            else:
                context_docs = ""

            response = text.run_summary_context(current_question, "", context_docs)
            print("response summary document files chat: ", response)

            response_data['answer_summary'] = response
            response_data['dataframe_json'] = None
            response_data['dataframe'] = None

        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return {'error': 'Internal server error'}, 500

    return response_data, 200