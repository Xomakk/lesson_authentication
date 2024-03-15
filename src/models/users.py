import sqlite3
import hashlib
from database.config import DB_FILE_URL


def hash_password(password):
    # Преобразуем пароль в байтовую строку
    password_bytes = password.encode("utf-8")
    # Создаем объект хеширования SHA-256
    sha256 = hashlib.sha256()
    # Обновляем объект хеширования байтами пароля
    sha256.update(password_bytes)
    # Получаем хеш пароля в шестнадцатеричном формате
    hashed_password = sha256.hexdigest()
    return hashed_password


class User:
    def __init__(self, id, username, password_hash=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return self.password_hash == hash_password(password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
        }


class UserManager:
    def create_user(self, username, password):
        con = sqlite3.connect(DB_FILE_URL)

        user = self.get_user_by_username(username)
        if user:
            return False  # пользователь не создан, т.к. уже существует

        password_hash = hash_password(password)
        SQL_CREATE_USER = f"""
            INSERT INTO users (username, password_hash)
            VALUES ('{username.lower()}', '{password_hash}')
        """

        con.execute(SQL_CREATE_USER)
        con.commit()
        return True  # пользователь создан

    def get_user_by_username(self, username):
        con = sqlite3.connect(DB_FILE_URL)

        SQL_SELECT = f'SELECT * from users WHERE username = "{username.lower()}"'
        query = con.execute(SQL_SELECT)
        user_data = query.fetchone()

        if user_data:
            return User(*user_data)
        return None
