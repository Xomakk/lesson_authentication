import secrets
from flask import Flask, redirect, render_template, request, session

from database.config import create_tables
from models.posts import PostManager
from models.users import UserManager
from utils import get_user_from_session

# Создаем и настраиваем приложение
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# создаем таблицы в БД
create_tables()


@app.route("/")
def home_page():
    posts = PostManager().get_all_posts()

    user = get_user_from_session()

    return render_template("index.html", posts=posts, user=user)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username, password = request.form.get("username"), request.form.get("password")
        remember_me = request.form.get("remember_me")
        user = UserManager().get_user_by_username(username)
        if user:
            if user.check_password(password):
                session["user"] = user.to_dict()

                if remember_me:
                    session.permanent = True

                return redirect("/")

            return render_template("login.html", error="Неправильный логин или пароль.")

        return render_template("login.html", error="Пользователь не найден.")


@app.route("/registration", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return render_template("register.html", error="Пароли не совпадают.")

        registration = UserManager().create_user(username, password)
        if registration:
            return redirect("/login")

        return render_template("register.html", error="Пользователь уже существует.")


@app.route("/profile", methods=["GET", "POST"])
def profile_page():
    user = get_user_from_session()
    if not user:
        return redirect("/login")

    if request.method == "GET":
        posts = PostManager().get_posts_by_username(user.username)
        return render_template("profile.html", posts=posts, user=user)

    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")

        PostManager().create_post(title, text, user.id)
        posts = PostManager().get_posts_by_username(user.username)
        return render_template("profile.html", posts=posts, user=user)


@app.route("/logout")
def logout_page():
    session.pop("user")
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
