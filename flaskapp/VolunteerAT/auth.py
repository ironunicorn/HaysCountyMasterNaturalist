import functools

import bcrypt
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from VolunteerAT.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/user')
def user():
    if g.user:
        return g.user
    else:
        return { 'id': None }

def get_user_by_email(email):
    '''Search database for user by email address.'''
    user = None
    with get_db() as cursor:
        cursor.execute(
            """SELECT id, password FROM master_naturalist WHERE email = %(email)s""",
            {'email': email}
        )

        user = cursor.fetchone()

    return user

def signin(user_id):
    session.clear()
    session['user_id'] = user_id
    return redirect(url_for('index'))

@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # hash and salt password.
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                with get_db() as cursor:
                    cursor.execute(
                        """INSERT INTO master_naturalist (email, password)
                            VALUES (%(email)s, %(hashed_password)s)""",
                        {'email': email, 'hashed_password': hashed_password}
                    )
            except:
                error = f"Oops! Something went wrong. Please try again."
            else:
                user = get_user_by_email(email)
                return signin(user[0])
        flash(error)

    return render_template('auth/signup.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        error = None
        user = get_user_by_email(email)
        if user is None:
            error = 'Incorrect email.'
        # check hashed and salted password.
        elif not bcrypt.checkpw(password, user[1]):
            error = 'Incorrect password.'

        if error is None:
            return signin(user[0])

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        with get_db() as cursor:
            cursor.execute(
                """SELECT id, email, admin, project_coordinator FROM master_naturalist WHERE id = %(user_id)s""",
                {'user_id': user_id}
            )
            user = cursor.fetchone()
            if not user:
                session.pop('user_id')
                g.user = None
            else:
                g.user = {'id': user[0], 'email': user[1], 'admin': user[2], 'project_coordinator': user[3]}


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def admin_required(view):
    '''Requires user be an admin or project_coordinator in order to access the
    decorated endpoint.'''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return {'error': 'login required'}, 400
        if not g.user['project_coordinator'] and not g.user['admin']:
            return {'error': 'access denied'}, 400

        return view(**kwargs)

    return wrapped_view
