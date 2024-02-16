from app import app, findRoom, db
from app.findRoom import run
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.timeNow import getMonth, getDate, getYear
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Room, Comment
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    floor = request.args.get('floor')
    return render_template('index.html', Classrooms=run(floor=floor))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data

        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your changes have been saved.')

        return redirect(url_for('profile'))

    return render_template('profile.html', form=form)


@app.route('/room/<floor_number>/<room_number>')
def room_detail(floor_number, room_number):
    room = Room.query.filter_by(floor=floor_number, number=room_number).first()
    comments = Comment.query.filter_by(room_id=room.id).all()

    return render_template('room.html', room=room, comments=comments)


if __name__ == '__main__':
    app.run(host="0.0.0.0")