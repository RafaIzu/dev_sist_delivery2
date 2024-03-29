import click
from flask_migrate import Migrate
import os
from app import create_app, db
from app.models import User, Destiny, Product, Theme, Role, Permission,\
    Category, Brand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Destiny=Destiny,
                Product=Product, Theme=Theme, Brand=Brand, Category=Category,
                Role=Role, Permission=Permission)

@app.cli.command()
# @click.argument('test_names', nargs=-1)
def test():
    """""Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)