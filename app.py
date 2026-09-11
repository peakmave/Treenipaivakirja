import sqlite3
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "dev-secret-key-vaihda-tuotannossa"
DATABASE = "database.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("workouts"))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
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
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Väärä käyttäjänimi tai salasana.")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("workouts"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/workouts")
@login_required
def workouts():
    db = get_db()
    query = request.args.get("q", "").strip()

    if query:
        rows = db.execute(
            """SELECT * FROM workouts
               WHERE user_id = ? AND (type LIKE ? OR notes LIKE ?)
               ORDER BY date DESC""",
            (session["user_id"], f"%{query}%", f"%{query}%"),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM workouts WHERE user_id = ? ORDER BY date DESC",
            (session["user_id"],),
        ).fetchall()

    return render_template("workouts.html", workouts=rows, query=query)


@app.route("/workouts/new", methods=["GET", "POST"])
@login_required
def new_workout():
    if request.method == "POST":
        date = request.form["date"]
        type_ = request.form["type"].strip()
        duration = request.form["duration"] or None
        notes = request.form.get("notes", "").strip()

        if not date or not type_:
            flash("Päivämäärä ja laji ovat pakollisia.")
            return render_template("workout_form.html", workout=None)

        db = get_db()
        db.execute(
            """INSERT INTO workouts (user_id, date, type, duration, notes)
               VALUES (?, ?, ?, ?, ?)""",
            (session["user_id"], date, type_, duration, notes),
        )
        db.commit()
        return redirect(url_for("workouts"))

    return render_template("workout_form.html", workout=None)


@app.route("/workouts/<int:workout_id>/edit", methods=["GET", "POST"])
@login_required
def edit_workout(workout_id):
    db = get_db()
    workout = db.execute(
        "SELECT * FROM workouts WHERE id = ? AND user_id = ?",
        (workout_id, session["user_id"]),
    ).fetchone()

    if workout is None:
        flash("Treeniä ei löytynyt.")
        return redirect(url_for("workouts"))

    if request.method == "POST":
        date = request.form["date"]
        type_ = request.form["type"].strip()
        duration = request.form["duration"] or None
        notes = request.form.get("notes", "").strip()

        db.execute(
            """UPDATE workouts SET date = ?, type = ?, duration = ?, notes = ?
               WHERE id = ? AND user_id = ?""",
            (date, type_, duration, notes, workout_id, session["user_id"]),
        )
        db.commit()
        return redirect(url_for("workouts"))

    return render_template("workout_form.html", workout=workout)


@app.route("/workouts/<int:workout_id>/delete", methods=["POST"])
@login_required
def delete_workout(workout_id):
    db = get_db()
    db.execute(
        "DELETE FROM workouts WHERE id = ? AND user_id = ?",
        (workout_id, session["user_id"]),
    )
    db.commit()
    return redirect(url_for("workouts"))


if __name__ == "__main__":
    app.run(debug=True)
