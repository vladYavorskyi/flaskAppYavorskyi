

from flask import (
    render_template, request, redirect,
    url_for, flash
)
from flask_login import login_required, current_user

from . import rooms_bp
from app.database import db
from .models import Room, RoomType
from .forms import RoomForm, RoomSearchForm


@rooms_bp.route("/", methods=["GET", "POST"])
def list_rooms():
    form = RoomSearchForm()

    q = form.q.data if form.validate_on_submit() else request.args.get("q", "")

    sort = request.args.get("sort", "number")
    direction = request.args.get("direction", "asc")

    query = Room.query.join(RoomType)

    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(
                Room.number.ilike(like),
                Room.description.ilike(like),
                RoomType.name.ilike(like),
            )
        )

    sort_column = {
        "number": Room.number,
        "price": Room.price,
        "capacity": Room.capacity,
        "created": Room.created_at,
    }.get(sort, Room.number)

    if direction == "desc":
        sort_column = sort_column.desc()

    rooms = query.order_by(sort_column).all()

    return render_template(
        "rooms/list.html",
        rooms=rooms,
        form=form,
        q=q,
        current_sort=sort,
        current_direction=direction,
    )


@rooms_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_room():
    form = RoomForm()
    form.type_id.choices = [(t.id, t.name) for t in RoomType.query.order_by(RoomType.name)]

    if form.validate_on_submit():
        room = Room(
            number=form.number.data,
            price=form.price.data,
            capacity=form.capacity.data,
            is_available=form.is_available.data,
            description=form.description.data,
            type_id=form.type_id.data,
            owner=current_user,
        )

        db.session.add(room)
        db.session.commit()
        flash("Room created successfully!", "success")
        return redirect(url_for("rooms.room_detail", room_id=room.id))

    return render_template("rooms/form.html", form=form, form_title="Create room")


@rooms_bp.route("/<int:room_id>")
def room_detail(room_id):
    room = Room.query.get_or_404(room_id)
    return render_template("rooms/detail.html", room=room)


def _check_owner(room: Room):
    if room.owner_id != current_user.id:
        flash("You can edit only your own rooms.", "danger")
        return False
    return True


@rooms_bp.route("/<int:room_id>/edit", methods=["GET", "POST"])
@login_required
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)

    if not _check_owner(room):
        return redirect(url_for("rooms.room_detail", room_id=room.id))

    form = RoomForm(obj=room)
    form.type_id.choices = [(t.id, t.name) for t in RoomType.query.order_by(RoomType.name)]

    if form.validate_on_submit():
        room.number = form.number.data
        room.price = form.price.data
        room.capacity = form.capacity.data
        room.is_available = form.is_available.data
        room.description = form.description.data
        room.type_id = form.type_id.data

        db.session.commit()
        flash("Room updated successfully!", "success")
        return redirect(url_for("rooms.room_detail", room_id=room.id))

    return render_template("rooms/form.html", form=form, form_title="Edit room")


@rooms_bp.route("/<int:room_id>/delete", methods=["POST"])
@login_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)

    if not _check_owner(room):
        return redirect(url_for("rooms.room_detail", room_id=room.id))

    db.session.delete(room)
    db.session.commit()

    flash("Room deleted successfully!", "info")
    return redirect(url_for("rooms.list_rooms"))
