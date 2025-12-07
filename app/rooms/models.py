

from app.database import db
from datetime import datetime


class RoomType(db.Model):
    __tablename__ = "room_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    rooms = db.relationship("Room", back_populates="type", cascade="all, delete")


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)

    number = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(500))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    type_id = db.Column(db.Integer, db.ForeignKey("room_types.id"), nullable=False)
    type = db.relationship("RoomType", back_populates="rooms")


    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("User", back_populates="rooms")
