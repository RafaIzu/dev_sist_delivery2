from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm


db = SQLAlchemy()
bootstrap = Bootstrap()
def create_app():
    app = Flask(__name__)

    # db_url = 'localhost:5432'
    # db_name = 'delivery'
    # db_user = 'postgres'
    # db_password = 'toalha28'
    app.config['SECRET_KEY'] = 'super dupper hard'
    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///delivery.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    bootstrap.init_app(app)

    from .form import form as form_blueprint
    app.register_blueprint(form_blueprint)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .error import error as error_blueprint
    app.register_blueprint(error_blueprint)

    from .models import Consumer, Product

    return app

    