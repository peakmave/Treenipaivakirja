import db


def add_comment(workout_id, user_id, comment):
    sql = """INSERT INTO comments (workout_id, user_id, comment, created_at)
             VALUES (?, ?, ?, datetime('now', 'localtime'))"""
    db.execute(sql, [workout_id, user_id, comment])


def get_comments(workout_id):
    sql = """SELECT comments.comment, comments.created_at, users.username
             FROM comments, users
             WHERE comments.user_id = users.id
             AND comments.workout_id = ?
             ORDER BY comments.id"""
    return db.query(sql, [workout_id])
