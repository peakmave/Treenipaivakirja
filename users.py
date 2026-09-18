from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from db import get_db


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        password2 = request.form["password2"]

        if not username or not password:
            flash("Täytä kaikki kentät.")
            return render_template("register.html")

        if password != password2:
            flash("Salasanat eivät täsmää.")
            return render_template("register.html")

        db = get_db()
        existing = db.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()

        if existing:
            flash("Käyttäjänimi on jo varattu.")
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        db.commit()

        flash("Tunnus luotu, voit kirjautua sisään.")
        return redirect(url_for("users.login"))

    return render_template("register.html")


@users.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user is None or not check_password_hash(
            user["password_hash"], password
        ):
            flash("Väärä käyttäjänimi tai salasana.")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect(url_for("workouts.workouts"))

    return render_template("login.html")


@users.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
