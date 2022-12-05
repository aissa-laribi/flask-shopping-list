from flask import (
    Blueprint, flash, redirect, request, render_template, request, url_for
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
