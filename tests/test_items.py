import pytest
from shopping_list.db import get_db
from shopping_list.auth import load_logged_in_user
from flask import g, session


def test_create_delete_item(app, client):
    client.post('auth/register',
                           data={'username': 'a', 'password': 'a'})
    client.post('auth/login',
                           data={'username': 'a', 'password': 'a'})
    assert client.get('/items').status_code == 200
    response = client.post('/items',
                           data={'add-item':'apple','add-button':'Add'})
    response
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM item WHERE label ='apple'",
        ).fetchone != get_db().IntegrityError
    client.post('/items',data={'del-item':'apple','del-button':'Delete'})
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM item WHERE label ='apple'",
        ).fetchone != get_db().IntegrityError


    @pytest.mark.parametrize(('label','message'),('', b'You cannot add an empty item'))
    def test_create_item_validate_input(message):
        response = client.post('/items', data={'add-item':'','add-button':'Add'})

        assert response in message.data

def test_get_items(app, client, auth):
    auth.login()
    assert client.get('/items').status_code == 200
    client.post('/items',data={'add-item':'pear','add-button':'Add'})
    with app.app_context():
        get_db()
        cursor = get_db().cursor()
        items = cursor.execute("SELECT COUNT(id) FROM item")
        count = items.fetchone()[0]
        assert count == 1
        rows = cursor.execute("SELECT * FROM item").fetchall()
        for row in rows:
            assert 'pear' in row[2]
