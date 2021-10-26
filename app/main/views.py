from flask import Blueprint, render_template, session, request, redirect,\
    url_for, flash
from flask_login import login_required, current_user
from app import db
from . import main
from .forms import EditProfileAdminForm
from ..models import User, Role, Product, Brand, Category, Theme
from ..decorators import admin_required
from ..geoloc import Geolocalization


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.id.desc()).paginate(page=page, per_page=6)
    brands = Brand.query.join(Product, (Brand.id == Product.id)).all()
    themes = Theme.query.join(Product, (Theme.id == Product.id)).all()
    categories = Category.query.join(Product,
                                     (Category.id == Product.id)).all()
    return render_template('index.html', name=session.get('name'),
                           known=session.get('known', False),
                           products=products, brands=brands, themes=themes,
                           categories=categories)

@main.route('/product/<int:id>')
def single_page(id):
    product = Product.query.get_or_404(id)
    price = str(format(product.price, ".2f")).replace(".", ",")
    return render_template('products/single_page.html',
                           product=product, price=price)


@main.route('/filter_brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_brand_id = Brand.query.filter_by(id=id).first_or_404()
    # product_brands = Product.query.filter_by(brand_id=id)
    product_brands = Product.query.filter_by(brand_id=id).paginate(
            page=page, per_page=4)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    themes = Theme.query.join(Product, (Theme.id == Product.theme_id)).all()
    categories = Category.query.join(Product,
                                     (Category.id == Product.category_id)
                                     ).all()
    return render_template('index.html', product_brands=product_brands,
                           brands=brands, themes=themes, categories=categories,
                           get_brand_id=get_brand_id)

@main.route('/filter_theme/<int:id>')
def get_theme(id):
    page = request.args.get('page', 1, type=int)
    get_theme_id = Theme.query.filter_by(id=id).first_or_404()
    # product_themes = Product.query.filter_by(theme_id=id)
    product_themes = Product.query.filter_by(theme_id=id).paginate(
        page=page, per_page=4)
    themes = Theme.query.join(Product, (Theme.id == Product.theme_id)).all()
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product,
                                     (Category.id == Product.category_id)).all()
    return render_template('index.html', product_themes=product_themes,
                           themes=themes, brands=brands, categories=categories,
                           get_theme_id=get_theme_id)

@main.route('/filter_categories/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_category_id = Category.query.filter_by(id=id).first_or_404()
    # product_categories = Product.query.filter_by(category_id=id)
    product_categories = Product.query.filter_by(category_id=id).paginate(
        page=page, per_page=4)
    categories = Category.query.join(Product,
                                     (Category.id == Product.category_id)).all()
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    themes = Theme.query.join(Product, (Theme.id == Product.theme_id)).all()
    print(categories)
    return render_template('index.html', product_categories=product_categories,
                           categories=categories, brands=brands, themes=themes,
                           get_category_id=get_category_id)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    distance = 100000
    is_server_ok = 0 # se 0, eh falso
    geoloc = Geolocalization()
    lon, lat = geoloc.gimmie_loc(address=user.destiny.address,
                                 number=user.destiny.number,
                                 neighborhood=user.destiny.neighborhood,
                                 city=user.destiny.city,
                                 state=user.destiny.state)
    if lat == 404:
        print("Nominatim server error. Don't blame me...")
        lat, lon = (-23.5710819, -46.649922) # seria as cordenadas da loja.
    else:
        is_server_ok = 1
        print("Nominatim server is cool!")
        distance = geoloc.calculate_distance(lat, lon)
    print("my distance is")
    deliverable = distance < 20
    return render_template('user/user.html', user=user, latitude=lat,
                           longitude=lon, isdeliverable=deliverable,
                           server_status=is_server_ok)


@main.route('/user/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        print('Trying to change things here!')
        current_user.telephone = request.form['telephone']
        current_user.destiny.address = request.form['address']
        current_user.destiny.number = request.form['number']
        current_user.destiny.zipcode = request.form['zipcode']
        current_user.destiny.neighborhood = request.form['neighborhood']
        current_user.destiny.complement = request.form['complement']
        current_user.destiny.city = request.form['city']
        current_user.destiny.state = request.form['state']
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Seu seus dados foram atualizados.')
        return redirect(url_for('.user', username=user.username))
    return render_template('user/edit_profile.html', user=user)


@main.route('/user/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.cpf = form.username.data
        user.telephone = form.telephone.data
        user.destiny.zipcode = form.zipcode.data
        user.destiny.address = form.address.data
        user.destiny.number = form.number.data
        user.destiny.complement = form.complement.data
        user.destiny.neighborhood = form.neighborhood.data
        user.destiny.city = form.city.data
        user.destiny.state = form.state.data
        db.session.add(user)
        db.session.commit()
        flash('Seus dados foram atualizados.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.cpf.data = user.cpf
    form.telephone.data = user.telephone
    form.zipcode.data = user.destiny.zipcode
    form.address.data = user.destiny.address
    form.number.data = user.destiny.number
    form.complement.data = user.destiny.complement
    form.neighborhood.data = user.destiny.neighborhood
    form.city.data = user.destiny.city
    form.state.data = user.destiny.state
    return render_template('user/edit_profile.html', form=form, user=user)
