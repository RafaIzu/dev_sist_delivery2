from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import redirect

app = Flask(__name__)
db_url = 'localhost:5432'
db_name = 'delivery'
db_user = 'postgres'
db_password = 'toalha28'
app.config['SECRET_KEY'] = 'super dupper hard'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///delivery.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
class Consumer(db.Model):
    __tablename__ = 'consumer'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Float)
    description = db.Column(db.String(500))
    players = db.Column(db.Integer)
    age = db.Column(db.Integer)

    def __init__(self, name, price, description, players, age):
        self.name = name
        self.price = price
        self.description = description
        self.players = players
        self.age = age

class ConsumerForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    password = StringField('Senha', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditConsumerForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    password = StringField('Senha', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/consumer')
def consumer():
    # consumer = Consumer.query.all()
    consumers = Consumer.query.with_entities(Consumer.id, Consumer.name,
                                             Consumer.email)
    print(consumer) 
    return render_template('consumer/consumer.html', consumers=consumers)


# @app.route("/add_consumer", methods=["GET", "POST"])
# def add_consumer():
#     if request.method == 'POST':
#         consumer = Consumer(request.form['name'], request.form['email'],
#                             request.form['password'])
#         db.session.add(consumer)
#         db.session.commit()
#         return redirect(url_for('consumer'))
#     return render_template('consumer/add_consumer.html')

@app.route("/add_consumer", methods=["GET", "POST"])
def add_consumer():
    if request.method == 'POST':
        consumer = Consumer(request.form['name'], request.form['email'],
                            request.form['password'])
        db.session.add(consumer)
        db.session.commit()
        return redirect(url_for('consumer'))
    return render_template('consumer/add_consumer.html')


@app.route('/edit_consumer/<int:id>', methods=['GET', 'POST'])
def edit_consumer(id):
    consumer = Consumer.query.get(id)
    if request.method == 'POST':
        consumer.name = request.form['name']
        consumer.email = request.form['email']
        db.session.commit()
        print('comitou')
        return redirect(url_for('consumer'))
    return render_template('consumer/edit_consumer.html', consumer=consumer)

@app.route('/delete_consumer/<int:id>')
def delete_consumer(id):
    consumer = Consumer.query.get(id)
    db.session.delete(consumer)
    db.session.commit()
    return redirect(url_for('consumer'))


@app.route('/product')
def product():
    products = Product.query.all()
    print(product) 
    return render_template('product/product.html', products=products)


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == 'POST':
        product = Product(request.form['name'], request.form['price'],
                            request.form['description'],
                            request.form['players'], request.form['age'])
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product'))
    return render_template('product/add_product.html')


@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.description = request.form['description']
        product.players = request.form['players']
        product.age = request.form['age']
        db.session.commit()
        print('comitou')
        return redirect(url_for('product'))
    return render_template('product/edit_product.html', product=product)


@app.route('/delete_product/<int:id>')
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('erros/500.html'), 500

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)