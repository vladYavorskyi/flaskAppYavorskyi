import pytest
from app import create_app
from app.database import db
from app.posts.models import Post


@pytest.fixture()
def test_client():
    """Тестовий Flask-клієнт з окремою ізольованою БД"""
    app = create_app()

    # Використовуємо окрему, тимчасову БД
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

        # Створюємо 1 тестовий пост
        post = Post(title="Test Post", content="This is a test post.")
        db.session.add(post)
        db.session.commit()

        # Повертаємо клієнт
        yield app.test_client()

        # Після тестів: чистимо
        db.drop_all()


def test_posts_list_page(test_client):
    """Перевірка сторінки списку постів"""
    response = test_client.get("/posts/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Test Post" in html
    assert "Список постів" in html


def test_post_detail_page(test_client):
    """Перевірка сторінки одного поста"""
    response = test_client.get("/posts/1")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Test Post" in html
    assert "This is a test post." in html
