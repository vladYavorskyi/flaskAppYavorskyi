import pytest
from app import create_app
from app.database import db
from app.users.models import User


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_register_page_loads(client):
    response = client.get("/users/register")
    assert response.status_code == 200


def test_login_page_loads(client):
    response = client.get("/users/login")
    assert response.status_code == 200


def test_user_registration(client, app):
    data = {
        "username": "testuser",
        "email": "test@mail.com",
        "password": "password123",
        "confirm_password": "password123",
    }
    client.post("/users/register", data=data, follow_redirects=True)

    user = User.query.filter_by(username="testuser").first()
    assert user is not None


def test_user_login_logout(client, app):
    user = User(username="bob", email="bob@mail.com")
    user.set_password("123456")
    db.session.add(user)
    db.session.commit()

    login_data = {"username": "bob", "password": "123456"}
    response = client.post("/users/login", data=login_data, follow_redirects=True)
    assert b"Welcome" in response.data

    response = client.get("/users/logout", follow_redirects=True)
    assert b"Logged out" in response.data

    response = client.get("/users/profile")
    assert response.status_code == 302
