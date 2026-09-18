from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from db import get_db


workouts = Blueprint("workouts", __name__)


def login_required(view):
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("users.login"))
        return view(*args, **kwargs)

    return wrapped


@workouts.route("/workouts")
@login_required
def workouts_list():
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


@workouts.route("/workouts/new", methods=["GET", "POST"])
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

        return redirect(url_for("workouts.workouts_list"))

    return render_template("workout_form.html", workout=None)


@workouts.route("/workouts/<int:workout_id>/edit", methods=["GET", "POST"])
@login_required
def edit_workout(workout_id):
    db = get_db()

    workout = db.execute(
        "SELECT * FROM workouts WHERE id = ? AND user_id = ?",
        (workout_id, session["user_id"]),
    ).fetchone()

    if workout is None:
        flash("Treeniä ei löytynyt.")
        return redirect(url_for("workouts.workouts_list"))

    if request.method == "POST":
        date = request.form["date"]
        type_ = request.form["type"].strip()
        duration = request.form["duration"] or None
        notes = request.form.get("notes", "").strip()

        db.execute(
            """UPDATE workouts
               SET date = ?, type = ?, duration = ?, notes = ?
               WHERE id = ? AND user_id = ?""",
            (date, type_, duration, notes, workout_id, session["user_id"]),
        )
        db.commit()

        return redirect(url_for("workouts.workouts_list"))

    return render_template("workout_form.html", workout=workout)


@workouts.route("/workouts/<int:workout_id>/delete", methods=["POST"])
@login_required
def delete_workout(workout_id):
    db = get_db()

    db.execute(
        "DELETE FROM workouts WHERE id = ? AND user_id = ?",
        (workout_id, session["user_id"]),
    )
    db.commit()

    return redirect(url_for("workouts.workouts_list"))
