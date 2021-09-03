from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from ..models import Consumer, Destiny
from .. import db
from ..email import send_email


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         consumer = Consumer.query.filter_by(email=request.form['email']).first()
#         if consumer is not None and consumer.verify_password(request.form['password']):
#             # login_user(user, request.form['remember'])
#             login_user(consumer)
#             next = request.args.get('next')
#             if next is None or not next.startswith('/'):
#                 print('>>>banana<<<')
#                 print("is_authenticated: ", current_user.is_authenticated)
#                 print("is_confirmed: ", current_user.confirmed)
#                 next = url_for('main.index')
#             return redirect(next)
#         flash('Invalid username or password. ')
#     return render_template('auth/login.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        consumer = Consumer.query.filter_by(email=form.email.data.lower()).first()
        if consumer is not None and consumer.verify_password(request.form['password']):
            login_user(consumer, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                print('>>>banana<<<')
                print("is_authenticated: ", current_user.is_authenticated)
                print("is_confirmed: ", current_user.confirmed)
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password. ')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você fez logout.')
    return redirect(url_for('main.index'))


# @auth.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         print(">>> chcocococo !")
#         destiny = Destiny(address=request.form['address'],
#                           number=request.form['number'],
#                           zipcode=request.form['zipcode'])
#         consumer = Consumer(email=request.form['email'],
#                             username=request.form['username'],
#                             password=request.form['password'],
#                             destiny=destiny)
#         db.session.add(consumer)
#         db.session.commit()
#         token = consumer.generate_confirmation_token()
#         send_email(consumer.email, 'Confirm Your Account',
#                    'auth/email/confirm', user=consumer, token=token)
#         flash('A confirmation email has been sent to you by email.')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/register.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        destiny = Destiny(address=form.address.data,
                          number=form.number.data,
                          zipcode=form.zipcode.data)
        consumer = Consumer(email=form.email.data.lower(),
                            username=form.username.data,
                            password=form.password.data,
                            destiny=destiny)
        db.session.add(consumer)
        db.session.commit()
        token = consumer.generate_confirmation_token()
        send_email(consumer.email, 'Confirm Your Account',
                   'auth/email/confirm', user=consumer, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required  # isto está me fud#%ˆ
def confirm(token):
    print('>>>entrou na sala!')
    if current_user.confirmed:
        print('>>>Entrou <<<')
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        print('>>>Também entrou')
        flash('Você confirmou sua conta. Obrigado!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
                print('>>>Sakura<<<')
                return redirect('auth.unconfirmed')


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        print('>>>cherry<<<')
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm You Account',
               'auth/email/confirm', user=current_user,
               token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form =ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid Password')
    return render_template("auth/change_password.html", form=form)