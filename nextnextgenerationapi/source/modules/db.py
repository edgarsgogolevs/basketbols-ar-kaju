import os
import pyodbc  # type: ignore

connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

# TODO: create db user for api


class Db:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Db, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.establish_connection()
    
    def establish_connection(self):
        self.conn = pyodbc.connect(connection_string)

    def check_connection(self):
        try:
            self.conn.cursor().execute("SELECT 1")
        except pyodbc.Error:
            return self.establish_connection()
