from utils import execute_query_and_return_df, dataframe_to_json

class User:
    def __init__(self, name: str, role: str, id_user: str = None):
        self.name = name
        self.role = role
        self.id_user = id_user

    def get_name(self):
        return self.name

    def get_role(self):
        return self.role
    
    def get_id_user(self):
        return self.id_user

    def get_personal_data(self):
        username = self.get_name()
        id_user = self.get_id_user()
        if self.role == "Student":
            sql_query = f"SELECT * FROM student WHERE name = '{username}' AND id = '{id_user}'"
        elif self.role == "Instructor":
            sql_query = f"SELECT * FROM instructor WHERE name = '{username}' AND id = '{id_user}'"
        else:
            sql_query = None

        df = None
        if sql_query:
            try:
                df = execute_query_and_return_df(sql_query)
                df_json = dataframe_to_json(df)
            except Exception as e:
                df = None
            return df_json