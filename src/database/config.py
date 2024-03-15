import sqlite3

DB_FILE_URL = "./src/database/data.db"


def create_tables():
    print("============== ТАБЛИЦЫ СОЗДАНЫ =================")
    SQL_CREATE_TABLE_USERS = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """

    SQL_CREATE_TABLE_POSTS = """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            likes INTEGET DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES users(id)
        )
    """

    con = sqlite3.connect(DB_FILE_URL)
    con.execute(SQL_CREATE_TABLE_USERS)
    con.execute(SQL_CREATE_TABLE_POSTS)
    con.commit()
