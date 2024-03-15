import sqlite3

from database.config import DB_FILE_URL


class Post:
    def __init__(
        self, id, title, text, likes, created_at, author_id, author_username=None
    ):
        self.id = id
        self.title = title
        self.text = text
        self.likes = likes
        self.created_at = created_at
        self.author_id = author_id
        self.author_username = author_username


class PostManager:
    def create_post(self, title, text, author_id):
        con = sqlite3.connect(DB_FILE_URL)

        SQL_CREATE_POST = f"""
            INSERT INTO posts (title, text, author_id)
            VALUES ('{title}', '{text}', {author_id})
        """
        con.execute(SQL_CREATE_POST)
        con.commit()

    def get_posts_by_username(self, username):
        con = sqlite3.connect(DB_FILE_URL)

        SQL_GET_POSTS = f"""
            SELECT posts.id, title, text, likes, created_at, author_id, username FROM posts 
            LEFT JOIN users ON posts.author_id = users.id
            WHERE author_id = (
                SELECT id FROM users WHERE username = '{username}'
            )
        """
        query = con.execute(SQL_GET_POSTS)
        posts = []
        for data in query.fetchall():
            posts.append(Post(*data))
        return posts

    def get_all_posts(self):
        con = sqlite3.connect(DB_FILE_URL)

        SQL_GET_POSTS = """
            SELECT posts.id, title, text, likes, created_at, author_id, username 
            FROM posts 
            LEFT JOIN users ON posts.author_id = users.id
        """

        query = con.execute(SQL_GET_POSTS)
        posts = []
        for data in query.fetchall():
            posts.append(Post(*data))
        return posts
