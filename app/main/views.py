from flask import Blueprint, render_template, session
from . import main


@main.route('/')
def index():
    return render_template('index.html', name=session.get('name'), known=session.get('known', False))