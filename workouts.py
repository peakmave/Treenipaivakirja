import db


def add_workout(user_id, date, workout_type, duration, notes):
    sql = "INSERT INTO workouts (user_id, date, type, duration, notes) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [user_id, date, workout_type, duration, notes])


def get_workouts(user_id):
    sql = "SELECT * FROM workouts WHERE user_id = ? ORDER BY date DESC"
    return db.query(sql, [user_id])


def get_workout(workout_id):
    sql = "SELECT * FROM workouts WHERE id = ?"
    result = db.query(sql, [workout_id])
    return result[0] if result else None


def update_workout(workout_id, date, workout_type, duration, notes):
    sql = "UPDATE workouts SET date = ?, type = ?, duration = ?, notes = ? WHERE id = ?"
    db.execute(sql, [date, workout_type, duration, notes, workout_id])


def remove_workout(workout_id):
    sql = "DELETE FROM workouts WHERE id = ?"
    db.execute(sql, [workout_id])
