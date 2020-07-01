from . import users as app
from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from app import db
from app.models import User

@app.route("/")
@login_required
def index():
    if not current_user or current_user.is_anonymous:
        flash('You do have to access to this page. Please login before continuing.', 'info')
        return redirect(url_for('account.login'))
    users = [i for i in User.query.all() if i.id != current_user.id]
    return render_template("users.html", users=users)


@app.route("/users/follow/<int:id>")
def user_follow(id):
    user = User.query.get(id)
    current_user.follow(user)
    db.session.commit()
    flash(f"You have followed {user.name}", "success")
    return redirect(url_for("users.index"))


@app.route("/users/unfollow/<int:id>")
def user_unfollow(id):
    user = User.query.get(id)
    current_user.unfollow(user)
    db.session.commit()
    flash(f"You have unfollowed {user.name}", "success")
    return redirect(url_for("users.index"))
