# seed.py
from app import create_app
from app.database import db
from app.posts.models import Post
from app.database.models import Product

app = create_app()

with app.app_context():
    # Повністю дропнути і створити заново всі таблиці
    db.drop_all()
    db.create_all()

    # --- демо-продукти ---
    p1 = Product(
        name="Ноутбук Lenovo Legion 5",
        price=38000,
        description="Потужний ігровий ноутбук з RTX 3060."
    )
    p2 = Product(
        name="Смартфон Samsung S24",
        price=42000,
        description="Флагманський смартфон з AMOLED 120Hz."
    )
    p3 = Product(
        name="Навушники Sony WH-1000XM4",
        price=11500,
        description="Преміальні Bluetooth навушники з шумодавом."
    )

    # --- демо-пости ---
    post1 = Post(title="Test Post 1", content="Перший тестовий пост.")
    post2 = Post(title="Test Post 2", content="Другий тестовий пост.")
    post3 = Post(title="Test Post 3", content="Третій тестовий пост.")

    db.session.add_all([p1, p2, p3, post1, post2, post3])
    db.session.commit()

    print("Готово! Таблиці пересоздані, дані додано.")
