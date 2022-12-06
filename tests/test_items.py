import pytest
from shopping_list.db import get_db
from flask import g, session


def test_create_item(app, client):
    client.post('auth/register',
                           data={'username': 'a', 'password': 'a'})
    client.post('auth/login',
                           data={'username': 'a', 'password': 'a'})
    assert client.get('/items').status_code == 200
    response = client.post('/items',
                           data={'item':'apple','add-button':'Add'})
    response
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM item WHERE label ='apple'",
        ).fetchone != get_db().IntegrityError


    @pytest.mark.parametrize(('label','message'),('', b'You cannot add an empty item'))
    def test_create_item_validate_input(message):
        response = client.post('/items', data={'item':'','add-button':'Add'})

        assert response in message.data

def test_get_items(app, client):
    client.post('auth/register', data={'username': 'test', 'password': 'test'})
    client.post('auth/login', data={'username': 'test', 'password': 'test'})
    assert client.get('/items').status_code == 200
    apple = client.post('/items',data={'item':'apple','add-button':'Add'})
    apple
    pear = client.post('/items',data={'item':'pear','add-button':'Add'})
    pear
    with app.app_context():
        get_db()
        cursor = get_db().cursor()
        items = cursor.execute("SELECT COUNT(id) FROM item")
        count = items.fetchone()[0]
        assert count == 2
