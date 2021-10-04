from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db, photos
from app.models import User, Product, Destiny, Theme, Brand, Category
from . import products
from ..decorators import admin_required
from .forms import AddProduct, AddTheme, AddBrand, AddCategory, EditProduct
import secrets


# @products.route('/user')
# def user():
#     # users = User.query.with_entities(User.id, User.username,
#     #                                          User.email)
#     users = User.query.all()
#     return render_template('user/user.html', users=users)
#
#
# @products.route('/edit_destiny/<int:id>', methods=['GET', 'POST'])
# def edit_destiny(id):
#     user = User.query.get(id)
#     if request.method == 'POST':
#         user.destiny.address = request.form['address']
#         user.destiny.number = request.form['number']
#         user.destiny.zipcode = request.form['zipcode']
#         user.destiny.neighborhood = request.form['neighborhood']
#         user.destiny.complement = request.form['complement']
#         user.destiny.city = request.form['city']
#         user.destiny.state = request.form['state']
#         db.session.commit()
#         return redirect(url_for('products.user'))
#     return render_template('user/edit_profile.html', user=user)
#
#
# @products.route('/delete_user/<int:id>')
# def delete_user(id):
#     user = User.query.get(id)
#     db.session.delete(user)
#     db.session.commit()
#     return redirect(url_for('products.user'))


@products.route('/products_selection')
@admin_required
def product_selection():
    return render_template('admin/products_selection.html')


@products.route('/products')
@admin_required
def product():
    products = Product.query.all()
    return render_template('products/products.html', products=products)


# @products.route('/add_products', methods=["GET", "POST"])
# @admin_required
# def add_product():
#     theme = Theme()
#     themes = Theme.query.all()
#     brand = Brand()
#     brands = Brand.query.all()
#     category = Category()
#     categories = Category.query.all()
#     if request.method == 'POST':
#         theme_got = request.form['theme']
#         brand_got = request.form['brand']
#         category_got = request.form['category']
#         product = Product(name=request.form['name'],
#                           price=request.form['price'].replace(",", "."),
#                           description=request.form['description'],
#                           players=request.form['players'],
#                           age=request.form['age'],
#                           theme=theme.query.filter_by(name=theme_got).first(),
#                           brand=brand.query.filter_by(name=brand_got).first(),
#                           category=category.query.filter_by(name=category_got).first())
#         db.session.add(product)
#         db.session.commit()
#         return redirect(url_for('products.product'))
#     return render_template('products/add_products.html', themes=themes,
#                            brands=brands, categories=categories)

@products.route('/add_products', methods=["GET", "POST"])
@admin_required
def add_product():
    theme = Theme()
    brand = Brand()
    category = Category()
    form = AddProduct()
    if form.validate_on_submit():
        image = photos.save(request.files.get('image'),
                            name=secrets.token_hex(10) + ".")
        print(">>>", image)
        product = Product(name=form.name.data,
                          price=float(form.price.data.replace(",", ".")),
                          description=form.description.data,
                          players=form.players.data,
                          age=form.age.data,
                          image=image,
                          theme=theme.query.filter_by(id=form.theme.data).first(),
                          brand=brand.query.filter_by(id=form.brand.data).first(),
                          category=category.query.filter_by(id=form.category.data).first())
        db.session.add(product)
        db.session.commit()
        flash(f"O produto {form.name.data} foi adicionado com sucesso",
              "success")
        return redirect(url_for('products.product'))
    return render_template('products/add_products.html', form=form)


# @products.route('/edit_products/<int:id>', methods=['GET', 'POST'])
# @admin_required
# def edit_product(id):
#     product = Product.query.get(id)
#     theme = Theme()
#     themes = Theme.query.all()
#     brand = Brand()
#     brands = Brand.query.all()
#     category = Category()
#     categories = Category.query.all()
#     if request.method == 'POST':
#         product.name = request.form['name']
#         product.price = request.form['price']
#         product.description = request.form['description']
#         product.players = request.form['players']
#         product.age = request.form['age']
#         new_theme = theme.query.filter_by(name=request.form['theme']).first()
#         product.theme_id = new_theme.id
#         new_brand = brand.query.filter_by(name=request.form['brand']).first()
#         product.brand_id = new_brand.id
#         new_category = category.query.filter_by(name=request.form['category']).first()
#         product.category_id = new_category.id
#         db.session.add(product)
#         db.session.commit()
#         return redirect(url_for('products.product'))
#     return render_template('products/edit_products.html', product=product,
#                            themes=themes, categories=categories, brands=brands)

@products.route('/edit_products/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = EditProduct()
    if form.validate_on_submit():
        image = request.files.get('image')
        print(">>> ", image.filename)
        product.name = form.name.data
        product.price = float(form.price.data.replace(",", "."))
        product.description = form.description.data
        product.players = form.players.data
        product.age = form.age.data
        product.image = image.filename
        product.theme_id = form.theme.data
        product.brand_id = form.theme.data
        product.category_id = form.category.data
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products.product'))
    form.name.data = product.name
    form.price.data = str(product.price).replace(".", ",")
    form.description.data = product.description
    form.players.data = product.players
    form.age.data = product.age
    form.theme.data = Theme.query.get(product.theme_id).name
    form.brand.data = Brand.query.get(product.brand_id).name
    form.category.data = Category.query.get(product.category_id).name
    return render_template('products/edit_products.html', form=form, product=product)

@products.route('/delete_products/<int:id>')
@admin_required
def delete_product(id):
    product = Product.query.get(id)
    product_name = product.name
    db.session.delete(product)
    db.session.commit()
    flash(f"O produto {product_name} foi removido com sucesso!", "success")
    return redirect(url_for('products.product'))


@products.route('/themes')
@admin_required
def theme():
    themes = Theme.query.all()
    return render_template('products/themes.html', themes=themes)


# @products.route("/add_themes", methods=["GET", "POST"])
# @admin_required
# def add_theme():
#     themes = Theme.query.all()
#     if request.method == 'POST':
#         theme = Theme(name=request.form['name'])
#         db.session.add(theme)
#         db.session.commit()
#         return redirect(url_for('products.theme'))
#     return render_template('products/add_themes.html', themes=themes)

@products.route("/add_themes", methods=["GET", "POST"])
@admin_required
def add_theme():
    form = AddTheme()
    if form.validate_on_submit():
        theme = Theme(name=form.name.data)
        db.session.add(theme)
        db.session.commit()
        flash(f"O tema {form.name.data} foi adicionado com sucesso.",
              "success")
        return redirect(url_for('products.theme'))
    return render_template('products/add_themes.html', form=form)

@products.route('/delete_themes/<int:id>')
@admin_required
def delete_theme(id):
    theme = Theme.query.get(id)
    theme_name = theme.name
    db.session.delete(theme)
    db.session.commit()
    flash(f"O tema {theme_name} foi removido com sucesso!", "success")
    return redirect(url_for('products.theme'))

@products.route('/brands')
@admin_required
def brand():
    brands = Brand.query.all()
    return render_template('products/brands.html', brands=brands)


# @products.route("/add_brands", methods=["GET", "POST"])
# @admin_required
# def add_brand():
#     brands = Brand.query.all()
#     if request.method == 'POST':
#         brand = Brand(name=request.form['name'])
#         db.session.add(brand)
#         db.session.commit()
#         return redirect(url_for('products.brand'))
#     return render_template('products/add_brands.html', brands=brands)

@products.route("/add_brands", methods=["GET", "POST"])
@admin_required
def add_brand():
    form = AddBrand()
    if form.validate_on_submit():
        brand = Brand(name=form.name.data)
        db.session.add(brand)
        db.session.commit()
        flash(f"A marca {form.name.data} foi adicionada com sucesso.",
              "success")
        return redirect(url_for('products.brand'))
    return render_template('products/add_brands.html', form=form)


@products.route('/delete_brands/<int:id>')
@admin_required
def delete_brand(id):
    brand = Brand.query.get(id)
    brand_name = brand.name
    db.session.delete(brand)
    db.session.commit()
    flash(f"A marca {brand_name} foi removida com sucesso.",
          "success")
    return redirect(url_for('products.brand'))


@products.route('/categories')
@admin_required
def category():
    categories = Category.query.all()
    return render_template('products/categories.html', categories=categories)


# @products.route("/add_categories", methods=["GET", "POST"])
# def add_category():
#     categories = Category.query.all()
#     if request.method == 'POST':
#         category = Category(name=request.form['name'])
#         db.session.add(category)
#         db.session.commit()
#         return redirect(url_for('products.category'))
#     return render_template('products/add_categories.html', categories=categories)


@products.route("/add_categories", methods=["GET", "POST"])
@admin_required
def add_category():
    form = AddCategory()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash(f"A categoria {form.name.data} foi adicionada com sucesso.",
              "success")
        return redirect(url_for('products.category'))
    return render_template('products/add_categories.html', form=form)

@products.route('/delete_categories/<int:id>')
def delete_category(id):
    category = Category.query.get(id)
    category_name = category.name
    db.session.delete(category)
    db.session.commit()
    flash(f"A categoria {category_name} foi removida com sucesso.",
          "success")
    return redirect(url_for('products.category'))