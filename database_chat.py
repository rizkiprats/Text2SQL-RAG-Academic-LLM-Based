from lib import Text2SQLRAG, TextRAG
from utils import dataframe_to_json, json_to_dataframe
import json

def chat_database_context(text2sql :Text2SQLRAG, text: TextRAG, 
    last_response, last_data_json, current_question):
    # Initialize response data
    response_data = {
        # 'sql_query': sql_query,
        # 'reasoning': reasoning,
        'dataframe': None,
        'answer_summary': '',
        'dataframe_json': None
    }

    if last_response is not None and last_data_json is not None:
        is_related = text.run_related_context_check(current_question, last_response, last_data_json)
        print("is_related : ", is_related)

        if is_related:
            try:
                df = json_to_dataframe(last_data_json)
                if (df is not None):
                    print("jumlah baris data : ", len(df))
                    if (len(df) == 1):
                        response_data['dataframe_json'] = json.loads(last_data_json)
                        response = text.run_summary_context(current_question, last_response, last_data_json)
                        print("response summary database chat related : ", response)

                        response_data['answer_summary'] = response
                        response_data['dataframe_json'] = json.loads(last_data_json)
                        response_data['dataframe'] = df

                    elif (len(df) > 1):
                        response_data['dataframe_json'] = json.loads(last_data_json)
                        response = text.run_summary_context(current_question, last_response, last_data_json)
                        print("response summary database chat related : ", response)

                        response_data['answer_summary'] = response
                        response_data['dataframe_json'] = json.loads(last_data_json)
                        response_data['dataframe'] = df
                else:
                    response = text.run_summary_context(current_question, last_response, None)
                    print("response summary database chat related : ", response)

                    response_data['answer_summary'] = response
                    response_data['dataframe_json'] = None
                    response_data['dataframe'] = None

            except Exception as e:
                print(f"Error processing request: {str(e)}")
                return {'error': 'Internal server error'}, 500
        else:
            try:
                # Process the message sql generate
                df, error = text2sql.run_sql_rag(current_question)

                if df is not None and not df.empty:
                    print("jumlah baris data : ", len(df))
                    if (len(df) == 1):
                        df_json = dataframe_to_json(df)
                        
                        response = text.run_summary_context(current_question, "", df_json)
                        print("response summary database chat not related : ", response)

                        response_data['answer_summary'] = response
                        response_data['dataframe_json'] = json.loads(df_json)
                        response_data['dataframe'] = df

                    elif (len(df) > 1):
                        df_json = dataframe_to_json(df)

                        response = text.run_summary_context(current_question, "", df_json)
                        print("response summary database chat not related : ", response)

                        response_data['answer_summary'] = response
                        response_data['dataframe_json'] = json.loads(df_json)
                        response_data['dataframe'] = df
                else:
                    # Generate summary for data empty
                    response = text.run_summary_context(current_question, "", None)
                    print("response summary database chat not related : ", response)

                    response_data['answer_summary'] = response
                    response_data['dataframe_json'] = None
                    response_data['dataframe'] = None

            except Exception as e:
                print(error)
                print(f"Error processing request: {str(e)}")
                return {'error': 'Internal server error'}, 500
    else:
        try:
            # Process the message sql generate
            df, error = text2sql.run_sql_rag(current_question)

            if df is not None and not df.empty:
                print("jumlah baris data : ", len(df))
                if (len(df) == 1):
                    df_json = dataframe_to_json(df)
                    response = text.run_summary_context(current_question, "", df_json)
                    print("response summary database chat: ", response)

                    response_data['answer_summary'] = response
                    response_data['dataframe_json'] = json.loads(df_json)
                    response_data['dataframe'] = df

                elif (len(df) > 1):
                    df_json = dataframe_to_json(df)
                    response = text.run_summary_context(current_question, "", df_json)
                    print("response summary database chat: ", response)

                    response_data['answer_summary'] = response
                    response_data['dataframe_json'] = json.loads(df_json)
                    response_data['dataframe'] = df
            else:
                # Generate summary for data empty
                response = text.run_summary_context(current_question, "", df_json)
                print("response summary database chat: ", response)

                response_data['answer_summary'] = response
                response_data['dataframe_json'] = None
                response_data['dataframe'] = None

        except Exception as e:
            print(error)
            print(f"Error processing request: {str(e)}")
            return {'error': 'Internal server error'}, 500
        
    return response_data, 200 