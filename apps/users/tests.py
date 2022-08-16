import pytest
from alembic.config import Config
from flask_migrate import upgrade
import pathlib

from app import create_app
from config.config import TestConfig


basedir = pathlib.Path(__file__).parent.parent.parent

@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        config = Config()

        config.set_main_option("script_location", "migrations")
        upgrade(config.get_main_option("migrations"))
    # other setup can go here

    yield app

    # clean up / reset resources here
    db_file = basedir / 'test_database.db'
    db_file.unlink()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_user_register(client):
    response = client.post(
        "/api/users/register/",
        data={
            "email": "testuser@gmail.com",
            "password": "test-password",
            "role": "000001",
        },
    )
    print(response)
    assert response.status_code == 201


def test_non_existence_user_login(client):
    response = client.post(
        "/api/users/login/",
        data={
            "email": "testuser@gmail.com",
            "password": "test-password",
        },
    )
    print(response)
    assert response.status_code == 401


def test_existence_user_login(client):
    test_user_register(client)
    response = client.post(
        "/api/users/login/",
        data={
            "email": "testuser@gmail.com",
            "password": "test-password",
        },
    )
    print(response)
    assert response.status_code == 200