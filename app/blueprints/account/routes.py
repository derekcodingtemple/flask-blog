from . import account
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from app.models import User
from app import db
import sqlalchemy, werkzeug


@account.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember_me = request.form.get("remember_me")

        try:
            user = User.query.filter_by(email=email).first()
            if user.check_password(password):
                login_user(user, remember=remember_me)
                flash("Login accepted", "success")
                return redirect(url_for("index"))
            flash("Invalid user / pass combination", "warning")
            return render_template("login.html")
        except AttributeError as err:
            print(err)
            print("You have either an incorrect password, or maybe you are trying to login a user that doesn't exist.")

    return render_template("login.html")


@account.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # if User.query.filter_by(email=email).first():
        #     flash("That email is already in use.", "danger")
        #     return redirect(url_for("account.register"))

        if password != confirm_password:
            flash("Password and confirmation must be the same.", "danger")
            return redirect(url_for("account.register"))
        
        u = User(name=name, email=email, password=password)
        u.generate_password(u.password)

        db.session.add(u)
        db.session.commit()
        flash("User registration successful.", "success")
        return redirect(url_for("account.login"))
        # try:
        # except sqlalchemy.exc.IntegrityError as err:
        #     print(err)
        #     print("You've tried adding a user that already exists.")

        #     flash("That email is already in use.", "danger")
        #     return redirect(url_for("account.register"))

    return render_template("register.html")


@account.route("/logout", methods=["GET"])
@login_required
def logout():
    # Write try/except that checks if the current user is logged in or not. 
    # If they are, execute logout_user, otherwise throw Exception
    try:
        logout_user()
        flash("Logged out successfully", "info")
        return redirect(url_for("account.login"))
    except werkzeug.routing.BuildError:
        print("You must be logged in to continue.")
    except:
        print("Something went wrong. Try again.")
