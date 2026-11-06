import sqlite3
from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS review_sessions (
  session_id INTEGER PRIMARY KEY AUTOINCREMENT,
  filename TEXT NOT NULL,
  diff_summary TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS suggestions (
  suggestion_id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL REFERENCES review_sessions(session_id),
  source TEXT NOT NULL,
  file_path TEXT NOT NULL,
  line_number INTEGER,
  category TEXT NOT NULL,
  severity TEXT NOT NULL,
  comment TEXT NOT NULL,
  suggested_fix TEXT NOT NULL,
  fingerprint TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reviewer_feedback (
  feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
  suggestion_id INTEGER NOT NULL UNIQUE REFERENCES suggestions(suggestion_id),
  decision TEXT NOT NULL,
  feedback_note TEXT DEFAULT '',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        db = get_db()
        db.executescript(SCHEMA)
        db.commit()
