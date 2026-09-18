from flask import Flask, render_template, session, redirect, url_for, g

from db import get_db
from users import users
from workouts import workouts


app = Flask(__name__)
app.secret_key = "dev-secret-key-vaihda-tuotannossa"


app.register_blueprint(users)
app.register_blueprint(workouts)


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("workouts.workouts_list"))

    return render_template("index.html")


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)

    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(debug=True)
