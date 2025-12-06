from app.database import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    image = db.Column(db.String(255), default="myphoto.jpg")
    about_me = db.Column(db.String(500))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship("Post", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


    def set_password(self, password):
        from app.database import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        from app.database import bcrypt
        return bcrypt.check_password_hash(self.password, password)
