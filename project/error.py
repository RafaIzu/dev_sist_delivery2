from flask import Blueprint, render_template

error = Blueprint('error', __name__)


@error.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@error.errorhandler(500)
def internal_server_error(e):
    return render_template('erros/500.html'), 500