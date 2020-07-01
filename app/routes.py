from app import db, login_manager
from app.models import User, Post
from flask import render_template, request, redirect, url_for, flash, current_app as app
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        posts = current_user.followed_posts()
    else:
        posts = Post.query.order_by(Post.created_on).all()
    
    if request.method == "POST":
        post_body = request.form.get("post_body")
        p = Post(body=post_body, user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        flash("Post created.", "success")
        return redirect(url_for("index"))

    return render_template("index.html", posts=posts)


@app.route("/profile")
@login_required
def profile():
    posts = User.query.get(current_user.id).posts.all()
    return render_template("profile.html", posts=posts)


@app.route("/profile/post/<int:id>")
def profile_single(id):
    p = Post.query.get(id)
    post = p
    return render_template("profile-single.html", post=post)


@app.route("/post/<int:id>")
def index_single(id):
    post = Post.query.get(id)
    return render_template("index-single.html", post=post)