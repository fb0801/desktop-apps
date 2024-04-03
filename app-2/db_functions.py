import os
import sqlite3

database_dir = os.path.join(os.getcwd(), '.dbs')
app_database = os.path.join(database_dir, 'app_db.db')


# Create the database or a database table
def create_database_or_database_table(table_name: str):
    connection = sqlite3.connect(app_database)
    cursor = connection.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (song TEXT)""")
    connection.commit()
    connection.close()



# Add a song to a database table
def add_song_to_database_table(song: str, table: str):
    connection = sqlite3.connect(app_database)
    cursor = connection.cursor()
    cursor.execute(f"""INSERT INTO {table} VALUES (?)""", (song,))
    connection.commit()
    connection.close()