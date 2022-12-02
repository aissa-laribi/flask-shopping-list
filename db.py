import sqlite3
from flask import g, current_app


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
    return g.db


def close(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
