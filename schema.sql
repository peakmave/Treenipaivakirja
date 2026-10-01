CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE workouts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users,
    date TEXT NOT NULL,
    type TEXT NOT NULL,
    duration INTEGER,
    notes TEXT
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO categories (name) VALUES ('Voimaharjoittelu'), ('Kestävyys'), ('Liikkuvuus'), ('Muu');

CREATE TABLE workout_categories (
    workout_id INTEGER REFERENCES workouts,
    category_id INTEGER REFERENCES categories,
    PRIMARY KEY (workout_id, category_id)
);
