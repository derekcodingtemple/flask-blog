from app import app, db, login_manager
from app.models import User, Post
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        posts = Post.query.order_by(Post.created_on).all()
        return render_template("index.html", posts=posts)
    elif request.method == "POST":
        post_body = request.form.get("post_body")
        p = Post(body=post_body, user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        flash("Post created.", "success")
        return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember_me = request.form.get("remember_me")

        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                login_user(user, remember=remember_me)
                flash("Login accepted", "success")
                return redirect(url_for("index"))
        flash("Invalid user / pass combination", "warning")
        return render_template("login.html")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if User.query.filter_by(email=email).first():
            flash("That email is already in use.", "danger")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Password and confirmation must be the same.", "danger")
            return redirect(url_for("register"))
        u = User(name=name, email=email, password=password)
        u.generate_password(u.password)

        db.session.add(u)
        db.session.commit()
        flash("User registration successful.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))


@app.route("/profile")
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
    p = Post.query.get(id)
    post = p
    return render_template("index-single.html", post=post)


@app.route("/users")
def users():
    users = [i for i in User.query.all() if i.id != current_user.id]
    return render_template("users.html", users=users)


@app.route("/users/follow/<int:id>")
def user_follow(id):
    user = User.query.get(id)
    current_user.follow(user)
    db.session.commit()
    flash(f"You have followed {user.name}", "success")
    return redirect(url_for("users"))


@app.route("/users/unfollow/<int:id>")
def user_unfollow(id):
    user = User.query.get(id)
    current_user.unfollow(user)
    db.session.commit()
    flash(f"You have unfollowed {user.name}", "success")
    return redirect(url_for("users"))
