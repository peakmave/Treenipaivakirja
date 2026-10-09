import secrets
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, redirect, session, flash, abort

import comments
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


def validate_registration(username, password, password2):
    error = None
    if not username or not password:
        error = "Täytä kaikki kentät."
    elif len(username) > 50:
        error = "Käyttäjänimi on liian pitkä."
    elif len(password) < 4:
        error = "Salasanan pitää olla vähintään 4 merkkiä."
    elif password != password2:
        error = "Salasanat eivät täsmää."
    return error


def validate_workout(date, workout_type, duration, notes, category_ids):
    valid_ids = [str(c["id"]) for c in workouts.get_all_categories()]
    error = None
    if not date or not workout_type:
        error = "Päivämäärä ja laji ovat pakollisia."
    elif not valid_date(date):
        error = "Päivämäärän pitää olla muotoa VVVV-KK-PP."
    elif len(workout_type) > 50:
        error = "Lajin nimi on liian pitkä."
    elif duration and (not duration.isdigit() or int(duration) > 1000):
        error = "Kesto pitää olla kokonaisluku 0-1000 minuuttia."
    elif len(notes) > 1000:
        error = "Muistiinpanot ovat liian pitkät."
    elif any(category_id not in valid_ids for category_id in category_ids):
        error = "Virheellinen luokka."
    return error


def render_workout_form(workout, selected):
    return render_template(
        "workout_form.html",
        workout=workout,
        all_categories=workouts.get_all_categories(),
        selected=selected,
    )


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

    error = validate_registration(username, password, password2)
    if error:
        flash(error)
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


@app.route("/workouts/<int:workout_id>")
def show_workout(workout_id):
    require_login()
    workout = workouts.get_workout(workout_id)
    if not workout:
        abort(404)

    return render_template(
        "workout.html",
        workout=workout,
        owner=users.get_user(workout["user_id"]),
        categories=workouts.get_workout_categories(workout_id),
        comments=comments.get_comments(workout_id),
    )


@app.route("/workouts/<int:workout_id>/comment", methods=["POST"])
def add_comment(workout_id):
    require_login()
    check_csrf()

    workout = workouts.get_workout(workout_id)
    if not workout:
        abort(404)

    comment = request.form["comment"].strip()
    if not comment:
        flash("Kommentti ei voi olla tyhjä.")
        return redirect(f"/workouts/{workout_id}")
    if len(comment) > 500:
        flash("Kommentti on liian pitkä.")
        return redirect(f"/workouts/{workout_id}")

    comments.add_comment(workout_id, session["user_id"], comment)
    return redirect(f"/workouts/{workout_id}")


@app.route("/workouts/new", methods=["GET", "POST"])
def new_workout():
    require_login()

    if request.method == "GET":
        return render_workout_form(None, [])

    check_csrf()
    date = request.form["date"]
    workout_type = request.form["type"].strip()
    duration = request.form["duration"]
    notes = request.form.get("notes", "").strip()
    category_ids = request.form.getlist("categories")

    error = validate_workout(date, workout_type, duration, notes, category_ids)
    if error:
        flash(error)
        return render_workout_form(None, category_ids)

    workout_id = workouts.add_workout(
        session["user_id"], date, workout_type, duration or None, notes
    )
    workouts.set_workout_categories(workout_id, category_ids)
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
        current = [str(c["id"]) for c in workouts.get_workout_categories(workout_id)]
        return render_workout_form(workout, current)

    check_csrf()
    date = request.form["date"]
    workout_type = request.form["type"].strip()
    duration = request.form["duration"]
    notes = request.form.get("notes", "").strip()
    category_ids = request.form.getlist("categories")

    error = validate_workout(date, workout_type, duration, notes, category_ids)
    if error:
        flash(error)
        return render_workout_form(workout, category_ids)

    workouts.update_workout(workout_id, date, workout_type, duration or None, notes)
    workouts.set_workout_categories(workout_id, category_ids)
    return redirect("/workouts")


@app.route("/workouts/<int:workout_id>/delete", methods=["GET", "POST"])
def delete_workout(workout_id):
    require_login()
    workout = workouts.get_workout(workout_id)

    if not workout:
        abort(404)
    if workout["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_workout.html", workout=workout)

    check_csrf()
    if "remove" in request.form:
        workouts.remove_workout(workout_id)
    return redirect("/workouts")


if __name__ == "__main__":
    app.run(debug=True)

@app.route("/users")
def show_users():
    require_login()
    all_users = users.get_all_users()
    return render_template("users.html", users=all_users)

@app.route("/users/<int:user_id>")
def show_user(user_id):
    require_login()
    user = users.get_user(user_id)
    if not user:
        abort(404)

    stats = workouts.get_user_stats(user_id)
    user_workouts = workouts.get_workouts(user_id)
    return render_template("user.html", profile_user=user, stats=stats, workouts=user_workouts)
