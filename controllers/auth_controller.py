from flask import flash, render_template, request, url_for, redirect
from flask_login import login_user, LoginManager, logout_user, current_user

from app import app, db
from models.user import User
from models.forms import LoginForm, UserRegister


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(alternative_id=user_id).first()


def login():
    # If app is in startup (no admin user found) show register page
    if app.config["FIRST_STARTUP"]:
        return redirect(url_for('auth_bp.register'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        remember = True if request.form.get("remember_me") else False

        user = User.find_by_username(username)

        # If user not found
        if not user:
            flash('Wrong Username or Password', 'error')
            return render_template("login.html", form=login_form)

        # Check the password
        if user.verify_pass(password):
            login_user(user, remember=remember)
            return redirect(url_for("home"))
        else:
            flash('Wrong Username or Password', 'error')

    return render_template("login.html", form=login_form)


def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))


def register():
    # If unauthenticated user try to load register page (when not app is not in startup)
    # show login page
    if not app.config["FIRST_STARTUP"]:
        if not current_user.is_authenticated:
            return redirect(url_for('auth_bp.login'))

    register_form = UserRegister()

    if register_form.validate_on_submit():
        fullname = request.form.get("fullname")
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        user = User(fullname=fullname,
                    username=username,
                    role=role)
        user.hash_pass(password)

        db.session.add(user)
        db.session.commit()

        # After creating admin user no need to see register page any more
        # set FIRST_STARTUP to false to load login page
        app.config["FIRST_STARTUP"] = False
        flash("Admin created.", "info")

        return redirect(url_for('auth_bp.login'))

    return render_template("register.html", form=register_form)


# def unauthorized_handler():
#     return render_template('home/page-403.html'), 403


# def access_forbidden(error):
#     return render_template('home/page-403.html'), 403


# def not_found_error(error):
#     return render_template('home/page-404.html'), 404


# def internal_error(error):
#     return render_template('home/page-500.html'), 500
