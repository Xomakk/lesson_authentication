from flask import session

from models.users import User


def get_user_from_session():
    user_data = session.get("user", None)

    if user_data:
        id = user_data.get("id")
        username = user_data.get("username")
        return User(id, username)

    return None
