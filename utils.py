import psycopg2
import pandas as pd
import json
from constant import DB_CONFIG

def execute_query_and_return_df(query, return_error=False):
    """
    Executes a SQL query on PostgreSQL and returns the results as a Pandas DataFrame.

    Args:
        query (str): The SQL query to execute.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the query results.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )

        df = pd.read_sql_query(query, conn)

        if return_error:
            return df, None
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        if return_error:
            return None, f"Error executing query: {str(e)}"
        return None
    finally:
        if conn:
            conn.close()

def dataframe_to_json(df: pd.DataFrame) -> str:
    """
    Convert a pandas DataFrame to a formatted JSON string.

    Args:
        df (pd.DataFrame): The DataFrame to convert

    Returns:
        str: Formatted JSON string representation of the DataFrame
    """
    if df is None or df.empty:
        return json.dumps({"message": "No data found"}, indent=2)

    # Convert DataFrame to dictionary
    data = df.to_dict(orient='records')

    # Convert to JSON with pretty printing
    json_str = json.dumps(data, indent=2, default=str)

    return json_str

def json_to_dataframe(json_str: str) -> pd.DataFrame:
    """
    Convert a JSON string to a pandas DataFrame.

    Args:
        json_str (str): The JSON string to convert.

    Returns:
        pd.DataFrame: A DataFrame representation of the JSON data.
    """
    try:
        # Parse the JSON string into a Python object
        data = json.loads(json_str)

        # Convert the parsed data into a DataFrame
        df = pd.DataFrame(data)

        return df
    except Exception as e:
        print(f"Error converting JSON to DataFrame: {e}")
        return pd.DataFrame()