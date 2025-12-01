from flask import render_template, redirect, url_for, request, flash
from . import posts_bp
from .models import Post
from .forms import PostForm
from app.database import db


@posts_bp.route("/")
def post_list():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("posts/posts.html", posts=posts)


@posts_bp.route("/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/detail_posts.html", post=post)


@posts_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(post)
        db.session.commit()

        flash("Пост створено!", "success")
        return redirect(url_for("posts.post_list"))

    return render_template("posts/add_post.html", form=form)


@posts_bp.route("/<int:post_id>/update", methods=["GET", "POST"])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        flash("Пост оновлено!", "success")
        return redirect(url_for("posts.post_detail", post_id=post.id))

    return render_template("posts/edit_posts.html", form=form, post=post)


@posts_bp.route("/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Пост видалено!", "success")
        return redirect(url_for("posts.post_list"))

    return render_template("posts/delete_confirm.html", post=post)
