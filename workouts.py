import db


def add_workout(user_id, date, workout_type, duration, notes):
    sql = "INSERT INTO workouts (user_id, date, type, duration, notes) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [user_id, date, workout_type, duration, notes])
    return db.last_insert_id()


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


def find_workouts(user_id, search_word):
    sql = "SELECT * FROM workouts WHERE user_id = ? AND (type LIKE ? OR notes LIKE ?) ORDER BY date DESC"
    like = "%" + search_word + "%"
    return db.query(sql, [user_id, like, like])


def get_all_categories():
    sql = "SELECT * FROM categories ORDER BY id"
    return db.query(sql)


def get_workout_categories(workout_id):
    sql = """SELECT categories.id, categories.name
             FROM categories, workout_categories
             WHERE categories.id = workout_categories.category_id
             AND workout_categories.workout_id = ?"""
    return db.query(sql, [workout_id])


def set_workout_categories(workout_id, category_ids):
    sql = "DELETE FROM workout_categories WHERE workout_id = ?"
    db.execute(sql, [workout_id])
    sql = "INSERT INTO workout_categories (workout_id, category_id) VALUES (?, ?)"
    for category_id in category_ids:
        db.execute(sql, [workout_id, category_id])


def get_user_stats(user_id):
    sql = "SELECT COUNT(*) count, COALESCE(SUM(duration), 0) total_duration FROM workouts WHERE user_id = ?"
    return db.query(sql, [user_id])[0]
