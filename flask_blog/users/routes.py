from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import current_user, logout_user, login_user, login_required
from flask_blog import db, bcrypt
from flask_blog.users.forms import RegistrationForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, LoginForm
from flask_blog.users.utils import send_reset_email, save_picture
from flask_blog.models import User, Post

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in', category="warning")
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can now log in', category="success")
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'You are already logged in', category="warning")
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash(f'Login Unsuccessful. Please check Email and Password.', category="danger")
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    flash(f'User logged out.', category="primary")
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data, form.username.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your Account has been updated ", category="success")
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', "POST"])
def reset_request():
    if current_user.is_authenticated:
        flash(f'You are already logged in', category="warning")
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", category="info")
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=['GET', "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        flash(f'You are already logged in', category="warning")
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(f'That is invalid or expired token', category="warning")
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You can now log in', category="success")
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset Password", form=form)


