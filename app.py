import sqlite3

from flask import Flask, render_template, request, redirect, session, flash

import users

app = Flask(__name__)
app.secret_key = "dev-secret-key-vaihda-tuotannossa"


@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/workouts")
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"].strip()
    password = request.form["password"]
    password2 = request.form["password2"]

    if not username or not password:
        flash("Täytä kaikki kentät.")
        return redirect("/register")
    if len(username) > 50:
        flash("Käyttäjänimi on liian pitkä.")
        return redirect("/register")
    if len(password) < 4:
        flash("Salasanan pitää olla vähintään 4 merkkiä.")
        return redirect("/register")
    if password != password2:
        flash("Salasanat eivät täsmää.")
        return redirect("/register")

    try:
        users.create_user(username, password)
    except sqlite3.IntegrityError:
        flash("Käyttäjänimi on jo varattu.")
        return redirect("/register")

    flash("Tunnus luotu, voit kirjautua sisään.")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]
    user_id = users.check_login(username, password)

    if not user_id:
        flash("Väärä käyttäjänimi tai salasana.")
        return redirect("/login")

    session["user_id"] = user_id
    session["username"] = username
    return redirect("/workouts")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
