from flask import Blueprint, render_template, session
from . import main
from ..models import User


@main.route('/')
def index():
    return render_template('index.html', name=session.get('name'),
                           known=session.get('known', False))

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)