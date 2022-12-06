from flask import (
    Blueprint, flash, render_template, request
)
from .auth import login_required, load_logged_in_user
from .db import get_db

bp = Blueprint('/', __name__)


@bp.route('/items', methods=['POST'])
@login_required
def create_item():
    item = request.form['item']
    db = get_db()
    error = None
    if item is None:  # For instance empty label
        error = 'You cannot add an empty item'
    if error is None:
        try:
            db.execute("INSERT INTO item (label) VALUES (?) ", (item,))
            db.commit()
        except db.IntegrityError:
            error = 'Item already in the list'
        else:
            return render_template('items.html')
        flash(error)
        
    return render_template('items.html')


@bp.route('/items', methods=['GET'])
@login_required
def get_items():
    load_logged_in_user()
    db = get_db()
    cursor = db.cursor()
    items = cursor.execute("SELECT * FROM item")
    rows = items.fetchall()
    for row in rows:
        print(row[0])
    return render_template('items.html', rows=rows)
