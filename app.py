import secrets
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, redirect, session, flash, abort

import users
import workouts

app = Flask(__name__)
app.secret_key = "dev-secret-key-vaihda-tuotannossa"


def require_login():
    if "user_id" not in session:
        abort(403)


def generate_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]


def check_csrf():
    token = request.form.get("csrf_token")
    if not token or token != session.get("csrf_token"):
        abort(403)


app.jinja_env.globals["csrf_token"] = generate_csrf_token


def valid_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/workouts")
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    check_csrf()
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

    check_csrf()
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


@app.route("/workouts")
def show_workouts():
    require_login()
    search_word = request.args.get("q", "").strip()

    if search_word:
        rows = workouts.find_workouts(session["user_id"], search_word)
    else:
        rows = workouts.get_workouts(session["user_id"])

    return render_template("workouts.html", workouts=rows, query=search_word)


@app.route("/workouts/new", methods=["GET", "POST"])
def new_workout():
    require_login()

    if request.method == "GET":
        return render_template("workout_form.html", workout=None)

    date = request.form["date"]
    workout_type = request.form["type"].strip()
    duration = request.form["duration"]
    notes = request.form.get("notes", "").strip()

    if not date or not workout_type:
        flash("Päivämäärä ja laji ovat pakollisia.")
        return render_template("workout_form.html", workout=None)
    if not valid_date(date):
        flash("Päivämäärän pitää olla muotoa VVVV-KK-PP.")
        return render_template("workout_form.html", workout=None)
    if len(workout_type) > 50:
        flash("Lajin nimi on liian pitkä.")
        return render_template("workout_form.html", workout=None)
    if duration and (not duration.isdigit() or int(duration) > 1000):
        flash("Kesto pitää olla kokonaisluku 0-1000 minuuttia.")
        return render_template("workout_form.html", workout=None)
    if len(notes) > 1000:
        flash("Muistiinpanot ovat liian pitkät.")
        return render_template("workout_form.html", workout=None)

    workouts.add_workout(session["user_id"], date, workout_type, duration or None, notes)
    return redirect("/workouts")



@app.route("/workouts/<int:workout_id>/edit", methods=["GET", "POST"])
def edit_workout(workout_id):
    require_login()
    workout = workouts.get_workout(workout_id)

    if not workout:
        abort(404)
    if workout["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("workout_form.html", workout=workout)

    date = request.form["date"]
    workout_type = request.form["type"].strip()
    duration = request.form["duration"]
    notes = request.form.get("notes", "").strip()

    if not date or not workout_type:
        flash("Päivämäärä ja laji ovat pakollisia.")
        return render_template("workout_form.html", workout=workout)
    if not valid_date(date):
        flash("Päivämäärän pitää olla muotoa VVVV-KK-PP.")
        return render_template("workout_form.html", workout=workout)
    if len(workout_type) > 50:
        flash("Lajin nimi on liian pitkä.")
        return render_template("workout_form.html", workout=workout)
    if duration and (not duration.isdigit() or int(duration) > 1000):
        flash("Kesto pitää olla kokonaisluku 0-1000 minuuttia.")
        return render_template("workout_form.html", workout=workout)
    if len(notes) > 1000:
        flash("Muistiinpanot ovat liian pitkät.")
        return render_template("workout_form.html", workout=workout)

    workouts.update_workout(workout_id, date, workout_type, duration or None, notes)
    return redirect("/workouts")


@app.route("/workouts/<int:workout_id>/delete", methods=["POST"])
def delete_workout(workout_id):
    require_login()
    workout = workouts.get_workout(workout_id)

    if not workout:
        abort(404)
    if workout["user_id"] != session["user_id"]:
        abort(403)

    workouts.remove_workout(workout_id)
    return redirect("/workouts")


if __name__ == "__main__":
    app.run(debug=True)
