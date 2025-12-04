from app.database import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


    tags = db.relationship(
        "Tag",
        secondary="post_tags",
        backref="posts"
    )


    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)


    user = db.relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post {self.title}>"
