from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from app.models import User
from app.forms import LoginForm
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))