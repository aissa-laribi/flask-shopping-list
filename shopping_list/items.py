from flask import (
    Blueprint, flash, render_template, request, redirect, url_for, g
)
from .auth import login_required, load_logged_in_user
from .db import get_db

bp = Blueprint('/', __name__)


@bp.route('/items', methods=['POST'])
@login_required
def create_delete_item():
    if request.method == "POST" and 'add-item' in request.form:
        item = request.form.get('add-item')
        db = get_db()
        error = None
        if item is None:  # For instance empty label
            error = 'You cannot add an empty item'
        if error is None:
            try:
                db.execute("INSERT INTO item (label, user_id) VALUES (?,?) ", (item, g.user['id']))
                db.commit()
                load_logged_in_user()
                return redirect(url_for('.get_items'))
            except db.IntegrityError:
                error = 'Item already in the list'
            else:
                pass
            flash(error)
    if request.method == "POST" and 'del-item' in request.form:
        item = request.form.get('del-item')
        db = get_db()
        error = None
        if item is None:  # For instance empty label
            error = 'Nothing to delete'
        if error is None:
            try:
                db.execute("DELETE FROM item WHERE label =(?) AND user_id =(?)",(item, g.user['id'],))
                db.commit()
                load_logged_in_user()
                return redirect(url_for('.get_items'))
            except db.IntegrityError:
                error = 'Item already in the list'
            else:
                pass
            flash(error)
        

@bp.route('/items', methods=['GET'])
@login_required
def get_items():
    load_logged_in_user()
    db = get_db()
    cursor = db.cursor()
    items = cursor.execute("SELECT * FROM item WHERE user_id=(?)",(g.user['id'],))
    rows = items.fetchall()
    return render_template('items.html', rows=rows)
