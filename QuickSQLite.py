import sqlite3
import os
import time

DANGEROUS_TEXT = ["DROP", "DATABASE", "TABLE", "1=1", "TRUE", "FALSE", "NULL", ";", "OR", "UNION", "--"]


def is_dangerous(text):
    for data in text:
        if data in DANGEROUS_TEXT:
            return True
    return False


class Database:  # class for making requests from a database
    def __init__(self, path):
        if os.path.isfile(path):
            if "/" in path:
                self.name = path.rsplit('/', 1)[1]
            else:
                self.name = path
            self.path = path
            self.conn = sqlite3.connect(path)
            self.cur = None
            self.recent_data = None
        else:
            raise Exception("QuickSQLite error - Database does not exist.")

    def __del__(self):  # to safely close database
        if self.cur is not None:
            self.cur.close()
        self.conn.close()

    def query(self, request, save_data=False):
        self.cur = self.conn.cursor()
        self.cur.execute(request)
        self.conn.commit()
        data = self.cur.fetchall()
        self.cur.close()
        self.cur = None
        if save_data:
            self.recent_data = data
            return data

    @staticmethod
    def _select(func):
        def wrapper(self, *args):
            self.cur = self.conn.cursor()
            query = func(self, *args)
            self.cur.execute(f"{query}")
            self.conn.commit()
            data = self.cur.fetchall()
            self.cur.close()
            self.cur = None
            self.recent_data = data
            return data
        return wrapper

    @_select
    def select(self, columns, table, clause=None):
        return f"SELECT {clause + " " if clause is not None else ""}{columns} FROM {table}"

    @_select
    def select_where(self, columns, table, where, clause=None):
        return f"SELECT {clause + " " if clause is not None else ""}{columns} FROM {table} WHERE {where}"

    @_select
    def select_orderby(self, columns, table, where, order, clause=None):
        return (f"SELECT {clause + " " if clause is not None else ""}{columns} "
                f"FROM {table} WHERE {where} ORDER BY {order}")

    @_select
    def select_join(self, columns, tables, where, group=False, having=False, clause=None):
        request_from = ""
        for table in tables:
            request_from += f"{table}, "
        request_from = request_from[:-2]
        if not group and not having:  # SELECT FROM WHERE
            request = (f"SELECT {clause + " " if clause is not None else ""}{columns} "
                       f"FROM {request_from} WHERE {where}")
        elif not group:  # SELECT FROM WHERE HAVING
            request = (f"SELECT {clause + " " if clause is not None else ""}{columns} "
                       f"FROM {request_from} WHERE {where} HAVING {having}")
        elif not having:  # SELECT FROM WHERE GROUP BY
            request = (f"SELECT {clause + " " if clause is not None else ""}{columns} "
                       f"FROM {request_from} where {where} GROUP BY {group}")
        else:  # SELECT FROM WHERE GROUP BY HAVING
            request = (f"SELECT {clause + " " if clause is not None else ""}{columns} "
                       f"FROM {request_from} WHERE {where} GROUP BY {group} HAVING {having}")
        return request

    @staticmethod
    def is_dangerous(text):
        for data in text:
            if data in DANGEROUS_TEXT:
                return True
        return False

    def update(self, table, columns, data, where="1=1"):
        sql_set = ""
        for column, item in zip(columns, data):
            sql_set += f"{column} = {item}, "
        sql_set = sql_set[:-2]
        query = f"UPDATE {table} SET {sql_set} WHERE {where}"
        self.cur = self.conn.cursor()
        self.cur.execute(query)
        self.conn.commit()
        self.cur.close()
        self.cur = None

    def delete(self, table, where=None):
        if where is None:
            query = f"DROP TABLE IF EXISTS {table}"
        elif type(where) is str:
            query = f"DELETE FROM {table} WHERE {where}"
        else:
            raise Exception("QuickSQLite error, you're dumb pls use strings for your where statements")
        self.cur = self.conn.cursor()
        self.cur.execute(query)
        self.conn.commit()
        self.cur.close()
        self.cur = None

    def insert(self, table, columns, data):
        label1 = "("
        label2 = "("
        for item in data:
            label1 += f"{item}, "
        for item in columns:
            label2 += f"{item}"
        label1 = label1[:-2] + ")"
        label2 = label2[:-2] + ")"
        query = f"INSERT INTO {table} {label2} VALUES {label1}"
        self.cur = self.conn.cursor()
        self.cur.execute(query)
        self.conn.commit()
        self.cur.close()
        self.cur = None

    def backup(self, path):
        path = path + str(time.asctime().replace(":", "-"))
        print(path)
        with open(self.path, "rb") as src_file:
            with open(path, "wb") as dst_file:
                dst_file.write(src_file.read())


class Column:
    def __init__(self, name):
        self.name = name
        self.data_type = None
        self.constraints = []

    def format_for_query(self):
        if " " not in self.name.strip():
            text = f"{self.name.strip()}"
        else:
            text = f"[{self.name}]"
        if self.data_type is not None:
            text += f" {self.data_type.upper()}"
        if len(self.constraints) > 0:
            for constraint in self.constraints:
                text += f" {constraint}"
        text += ", "
        return text


class Table:
    def __init__(self, name):
        self.name = name
        self.column_names = []
        self.columns = []

    def add_column(self, column):
        self.column_names.append(column.name)
        self.columns.append(column.format_for_query())

    def commit_to_database(self, database):
        columns = ""
        for column in self.columns:
            columns += column
        columns = columns[:-2]
        query = f"CREATE TABLE IF NOT EXISTS {self.name} ({columns})"
        database.cur = database.conn.cursor()
        database.cur.execute(query)
        database.conn.commit()
        database.cur.close()
        database.cur = None
