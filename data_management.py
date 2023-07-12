import pandas as pd
import os
import sys


# Removed SQL import, only used in development.
# from psycopg2 import sql
# from sqlalchemy import create_engine
# import socket
# import psycopg2

def load_data_from_file(file_path):
    df_output = pd.read_csv(file_path, header=0, delimiter=';')
    print("Data loaded.")
    return df_output


def get_executable_relative_path(*path_parts):
    """Generate a file path relative to the location of the executable."""

    # Check if we are running as a script or as a frozen exe
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # If we are running as a frozen exe, the executable is sys.executable
        base_dir = os.path.dirname(sys.executable)
    else:
        # If we are running as a script, the executable is this script itself
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate a file path relative to this directory
    path = os.path.join(base_dir, *path_parts)

    return path



def get_resource_path(relative_path):
    """ Get absolute path to resource, used for pyinstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# def setup_db(override_use_home_ip=False):
#     current_ip = socket.gethostbyname(socket.gethostname())
#     given_ip = "192.168.1"
#
#     if current_ip.startswith(given_ip) and override_use_home_ip:
#         print("Current IP is within Kerkstraat IP range.")
#         host_ip =
#     else:
#         print("Current IP is not within the Kerkstraat IP range.")
#         host_ip =
#     # Connect to the PostgreSQL database
#     connection = psycopg2.connect(
#         dbname=,
#         user=,
#         password=,
#         host=host_ip,
#         port=
#     )
#     cursor = connection.cursor()
#     return connection, cursor
#
#
# def create_postgresql_table_deprecated(df, table_name, connection, cursor):
#     # Check if table already exists
#     print("Checking if table already exists...")
#     cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", (table_name,))
#     table_exists = cursor.fetchone()[0]
#
#     # Create table if it doesn't already exist
#     if not table_exists:
#         print("Table does not exist, Creating table...")
#         cols = ", ".join(f"{col} varchar(255)" for col in df.columns)
#         cursor.execute(f"CREATE TABLE {table_name} ({cols})")
#         print("Table created!")
#
#     # Insert data into table
#     print("Starting value insertion...")
#     insert_statement = sql.SQL('INSERT INTO {} ({}) VALUES {}').format(
#         sql.Identifier(table_name),
#         sql.SQL(', ').join(map(sql.Identifier, df.columns)),
#         sql.SQL(', ').join(
#             sql.SQL('({})').format(sql.SQL(', ').join(sql.Placeholder() * len(df.columns)))
#             for row in df.to_numpy())
#     )
#
#     cursor.execute(insert_statement)
#     print("Query executed!")
#
#     # Commit changes and close connection
#     connection.commit()
#     cursor.close()
#     connection.close()
#
#     return
#
#
# def create_postgresql_table(df, table_name):
#     # Define the PostgreSQL engine using SQLAlchemy
#     engine = create_engine('')
#
#     try:
#         # Write the DataFrame to PostgreSQL table
#         df.to_sql(table_name, engine, if_exists='fail')
#     except ValueError as vx:
#         print(vx)
#         pass
#     return
#
#
# def df_from_postgres(table_name, cursor, columns=None):
#     # Check if no columns specified
#     if columns is None or not columns:
#         # Select all columns
#         select_stmt = f"SELECT * FROM {table_name}"
#     else:
#         # Select specified columns
#         cols = ", ".join(columns)
#         select_stmt = f"SELECT {cols} FROM {table_name}"
#
#     # Execute query and fetch results
#     cursor.execute(select_stmt)
#     rows = cursor.fetchall()
#
#     # Get column names from cursor description
#     col_names = [desc[0] for desc in cursor.description]
#
#     # Convert result to DataFrame
#     df = pd.DataFrame(rows, columns=col_names)
#
#     return df
#
#
# def load_data_from_db(table_name):
#     df = pd.read_sql_table(table_name, "")
#     print("Data loaded.")
#     return df


# def store_KRO_data(file_path_KRO):
#     df = pd.read_csv(file_path_KRO, header=0, delimiter=';')
#     print("Data loaded.")
#     create_postgresql_table(df, "KRO")
#     print("Data stored in PostgreSQL database table.")
#     return
