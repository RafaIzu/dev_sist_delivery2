from flask import Blueprint, render_template, session, request, redirect,\
    url_for, flash
from flask_login import login_required, current_user
from app import db
from . import main
from .forms import EditProfileAdminForm
from ..models import User, Role, Product, Brand, Category, Theme
from ..decorators import admin_required


@main.route('/')
def index():
    products = Product.query.all()
    brands = Brand.query.all()
    themes = Theme.query.all()
    categories = Category.query.all()
    return render_template('index.html', name=session.get('name'),
                           known=session.get('known', False),
                           products=products, brands=brands, themes=themes,
                           categories=categories)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user/user.html', user=user)


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
