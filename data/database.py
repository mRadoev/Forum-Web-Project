from mariadb import connect
from mariadb.connections import Connection
import sqlite3


def _get_connection() -> Connection:
    return connect(
        host='localhost',
        user='root',
        password='password',
        port=3306,
        database='forum_database1'
    )


def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def update_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount

#
# def query_count(sql: str, sql_params=()):
#     with connect(_db_file) as conn:
#         cursor = conn.cursor()
#         cursor.execute(sql, sql_params)
#
#         return cursor.fetchone()[0]


# def import_sql_script():
#     # Connect to SQLite database
#     conn = sqlite3.connect(_db_file)
#     cursor = conn.cursor()
#
#     # Read SQL script
#     with open(sql_script_file, 'r') as file:
#         sql_script = file.read()
#
#     # Execute SQL script
#     cursor.executescript(sql_script)
#
#     # Commit changes and close connection
#     conn.commit()
#     conn.close()
