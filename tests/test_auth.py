import pytest
from shopping_list.db import get_db
from flask import g, session


def test_register(client, app):
    assert client.get('auth/register').status_code == 200
    response = client.post('auth/register',
                           data={'username': 'a', 'password': 'a'})
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username ='a'",
        ).fetchone is not None

    @pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Username is required.'),
        ('a', '', b'Password is required.'),
        ('test', 'test', b'already registered'),
    ))
    def test_register_validate_input(client, username, password, message):
        response = client.post('auth/register',
                               data={'username': username,
                                     'password': password})
        assert message in response.data


def test_login(auth, client):
    assert client.get('auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == '/items'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

    @pytest.mark.parametrize(('username', 'password', 'message'), (
        ('a', 'test', b'Incorrect username.'),
        ('test', 'a', b'Incorrect username.'),
    ))
    def test_login_validate_input(auth, username, password, message):
        response = auth.login(username, password)
        assert message in response.data


def test_load_logged_in_user(client):
    with client:
        client.post('auth/login',
                    data={'username': 'test', 'password': 'test'})
        client.get('/')
        user_id = session.get('user_id')
        assert user_id == 1
        assert g.user['username'] == 'test'


def test_logout(client, auth):
    test_load_logged_in_user(client)
    response = auth.logout()
    assert response.headers["Location"] == '/auth/login'


def test_login_required(client):
    with client:
        response = client.get('/items')
        assert response.headers["Location"] == '/auth/login'
