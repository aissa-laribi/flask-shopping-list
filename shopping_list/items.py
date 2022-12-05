from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from shopping_list.auth import login_required
from shopping_list.db import get_db

bp = Blueprint('items', __name__)