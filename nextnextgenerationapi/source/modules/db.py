import os
import pyodbc  # type: ignore
import logging
from typing import Any, Union

# connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]
user = os.environ["AZURE_SQL_USER"]
password = os.environ["AZURE_SQL_PASSWORD"]
connection_string = 'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:basketball-devel.database.windows.net,1433;Database=baskteball-devel;Uid={0};Pwd={1};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
connection_string = connection_string.format(user, password)

# WARNING: None of these functions are tested


class Db:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Db, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.lg = logging.getLogger("api.db")
        self.conn = None
        self.conn_retry_count = 0
        self.establish_connection()

    def establish_connection(self):
        if self.conn_retry_count > 5:
            self.lg.error("Could not establish connection to database")
            raise Exception("Could not establish connection to database")
        try:
            self.lg.info("Establishing connection to database...")
            self.conn = pyodbc.connect(connection_string)
        except pyodbc.Error:
            self.lg.warning(f"Could not establish connection to database. Retrying...")
            self.conn_retry_count += 1
            return self.establish_connection()

    def check_connection(self):
        try:
            self.conn.cursor().execute("SELECT 1")  # type: ignore
        except pyodbc.Error:
            self.lg.warning("Connection to database lost")
            return self.establish_connection()

    def get_cursor(self):
        self.check_connection()
        if not self.conn:
            self.establish_connection()
        if not self.conn:
            raise Exception("Could not establish connection to database")
        return self.conn.cursor()

    def to_dictlist(self, data: list, description: list) -> list:
        ret = []
        columns = [x[0] for x in description]
        for row in data:
            ret.append(dict(zip(columns, row)))
        return ret

    def select(self, query: str, data: Union[list, tuple, None] = None) -> list[dict]:
        cursor = self.get_cursor()
        if isinstance(data, list) or isinstance(data, tuple):
            self.lg.debug(f'Executing query: "{query}" <= {data}')
            cursor.execute(query, data)
        else:
            self.lg.debug(f'Executing query: "{query}"')
            cursor.execute(query)
        return self.to_dictlist(cursor.fetchall(), cursor.description)


    def select_as_dict(self, query: str, data: Union[list, tuple, None] = None) -> dict:
        """
        Returns dict where key is first col and value is second col
        """
        self.check_connection()
        cursor = self.get_cursor()
        if isinstance(data, list) or isinstance(data, tuple):
            self.lg.debug(f'Executing query: "{query}" <= {data}')
            cursor.execute(query, data)
        else:
            self.lg.debug(f'Executing query: "{query}"')
            cursor.execute(query)
        ret = {}
        for row in cursor.fetchall():
            ret[row[0]] = row[1]
        return ret

    def insert_dict(self, table: str, data: dict) -> int:
        cursor = self.get_cursor()
        columns = ", ".join(data.keys())
        values = ", ".join(["?"] * len(data))
        ins_values = list(data.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.lg.debug(f'Executing query: "{query}" <= {ins_values}')
        cursor.execute(query, ins_values)
        self.conn.commit()
        return cursor.rowcount

    def update_dict(self, table: str, data: dict, where: dict) -> int:
        cursor = self.get_cursor()
        columns = ", ".join([f"{column} = ?" for column in data.keys()])
        where_q = " AND ".join([f"{column} = ?" for column in where.keys()])
        query = f"UPDATE {table} SET {columns} WHERE {where_q}"
        self.lg.debug(f'Executing query: "{query}" <= {data} <= {where}')
        cursor.execute(query, list(data.values()) + list(where.values()))
        self.conn.commit()
        return cursor.rowcount

    def delete_dict(self, table: str, where: dict) -> int:
        cursor = self.get_cursor()
        where_q = " AND ".join([f"{column} = ?" for column in where.keys()])
        query = f"DELETE FROM {table} WHERE {where_q}"
        self.lg.debug(f'Executing query: "{query}" <= {where}')
        cursor.execute(query, list(where.values()))
        self.conn.commit()
        return cursor.rowcount

    def insert_or_update_dict(self, table: str, upd: dict, where: dict) -> int:
        cursor = self.get_cursor()
        columns = ", ".join(
            [f"{column} = ?" for column in upd.keys()]
            + [f"{column} = ?" for column in where.keys()]
        )
        update_columns = ", ".join([f"{column} = ?" for column in upd.keys()])
        query = f"INSERT INTO {table} ({columns}) VALUES ({columns}) ON DUPLICATE KEY UPDATE {update_columns}"
        self.lg.debug(f'Executing query: "{query}" <= {upd} <= {where}')
        cursor.execute(
            query, list(upd.values()) + list(where.values()) + list(upd.values())
        )
        self.conn.commit()
        return cursor.rowcount
