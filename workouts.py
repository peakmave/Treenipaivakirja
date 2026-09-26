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
