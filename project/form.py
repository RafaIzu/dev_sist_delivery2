from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Consumer, Product

form = Blueprint('form', __name__)


@form.route('/consumer')
def consumer():
    # consumer = Consumer.query.all()
    consumers = Consumer.query.with_entities(Consumer.id, Consumer.name,
                                             Consumer.email)
    print(consumer) 
    return render_template('consumer/consumer.html', consumers=consumers)


@form.route("/add_consumer", methods=["GET", "POST"])
def add_consumer():
    if request.method == 'POST':
        consumer = Consumer(name=request.form['name'], email=request.form['email'],
                            password=generate_password_hash(request.form['password']))
        db.session.add(consumer)
        db.session.commit()
        return redirect(url_for('form.consumer'))
    return render_template('consumer/add_consumer.html')


@form.route('/edit_consumer/<int:id>', methods=['GET', 'POST'])
def edit_consumer(id):
    consumer = Consumer.query.get(id)
    if request.method == 'POST':
        consumer.name = request.form['name']
        consumer.email = request.form['email']
        db.session.commit()
        print('comitou')
        return redirect(url_for('form.consumer'))
    return render_template('consumer/edit_consumer.html', consumer=consumer)

@form.route('/delete_consumer/<int:id>')
def delete_consumer(id):
    consumer = Consumer.query.get(id)
    db.session.delete(consumer)
    db.session.commit()
    return redirect(url_for('form.consumer'))


@form.route('/product')
def product():
    products = Product.query.all()
    print(product) 
    return render_template('product/product.html', products=products)


@form.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == 'POST':
        product = Product(name=request.form['name'], price=request.form['price'],
                            description=request.form['description'],
                            players=request.form['players'], age=request.form['age'])
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('form.product'))
    return render_template('product/add_product.html')


@form.route('/edit_product/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('form.product'))
    return render_template('product/edit_product.html', product=product)


@form.route('/delete_product/<int:id>')
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('form.product'))
