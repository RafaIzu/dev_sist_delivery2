from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import User, Product, Destiny, Theme
from . import tables


@tables.route('/user')
def user():
    # users = User.query.with_entities(User.id, User.username,
    #                                          User.email)
    users = User.query.all()
    return render_template('user/user.html', users=users)


@tables.route('/edit_destiny/<int:id>', methods=['GET', 'POST'])
def edit_destiny(id):
    user = User.query.get(id)
    if request.method == 'POST':
        user.destiny.address = request.form['address']
        user.destiny.number = request.form['number']
        user.destiny.zipcode = request.form['zipcode']
        user.destiny.neighborhood = request.form['neighborhood']
        user.destiny.complement = request.form['complement']
        user.destiny.city = request.form['city']
        user.destiny.state = request.form['state']
        db.session.commit()
        return redirect(url_for('tables.user'))
    return render_template('user/edit_profile.html', user=user)


@tables.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('tables.user'))


@tables.route('/product')
def product():
    products = Product.query.all()
    return render_template('product/product.html', products=products)


@tables.route("/add_product", methods=["GET", "POST"])
def add_product():
    theme = Theme()
    themes = theme.query.all()
    if request.method == 'POST':
        theme_got = request.form['theme']
        product = Product(name=request.form['name'],
                          price=request.form['price'].replace(",", "."),
                          description=request.form['description'],
                          players=request.form['players'],
                          age=request.form['age'],
                          theme=theme.query.filter_by(name=theme_got).first())
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('tables.product'))
    return render_template('product/add_product.html', themes=themes)


@tables.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get(id)
    theme = Theme()
    themes = theme.query.all()
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.description = request.form['description']
        product.players = request.form['players']
        product.age = request.form['age']
        new_theme = theme.query.filter_by(name=request.form['theme']).first()
        print(">>>", new_theme.id)
        print("--->", product.theme.id)
        product.theme_id = new_theme.id
        db.session.commit()
        return redirect(url_for('tables.product'))
    return render_template('product/edit_product.html', product=product, themes=themes)


@tables.route('/delete_product/<int:id>')
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('tables.product'))
