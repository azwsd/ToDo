from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, get_flashed_messages
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask("__name__")

db = SQL("sqlite:///todo.db")

# Configure session to use filesystem and not cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Prevent response cache
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    rows = db.execute("SELECT * FROM todos WHERE user_id = ?;", session["user_id"])
    name = db.execute("SELECT username FROM users WHERE id = ?;", session["user_id"])
    name = name[0]["username"]
    if request.method == "POST":
        if request.form["btn"]=="add":
            todo = request.form.get("todo")
            if todo == "":
                flash("Please enter todo")
                return redirect(url_for('index'))
            db.execute("INSERT INTO todos(user_id, todo) VALUES(?, ?);", session["user_id"], todo)
            rows = db.execute("SELECT * FROM todos WHERE user_id = ?;", session["user_id"])
        else:
            id = request.form["id"]
            db.execute("DELETE FROM todos WHERE id = ? AND user_id = ?;", id, session["user_id"])
            return redirect(url_for('index'))
        return render_template("index.html", name=name, rows=rows)
    else:
        return render_template("index.html", name=name, rows=rows)


@app.route("/register", methods=["GET", "POST"])
def register():
    get_flashed_messages()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        users = db.execute("SELECT * FROM users WHERE username = ?;", username)

        if not username:
           flash("Please enter username")
           return redirect(url_for('register'))
        if len(users) > 0:
            flash("User already exists")
            return redirect(url_for('register'))
        if not password or not confirmation:
            flash("Please enter password and password confirmation")
            return redirect(url_for('register'))
        if password != confirmation:
            flash("Password and confirmation must match")
            return redirect(url_for('register'))

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    get_flashed_messages()

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            flash("must provide username")
            return redirect(url_for('login'))
        elif not request.form.get("password"):
             flash("must provide password")
             return redirect(url_for('login'))
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password")
            return redirect(url_for('login'))

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/remove", methods=["POST"])
def remove():
    id = request.form["id"]
    print(id)
    return redirect("/")