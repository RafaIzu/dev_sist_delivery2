import os
from flask import redirect, render_template, url_for, flash, request, session
from flask_login import current_user
from . import cart
from ..models import Product, User
from ..mercadopago import Payment
from ..geoloc import Geolocalization

def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


def calculate_freight():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first_or_404()
        geoloc = Geolocalization()
        lon, lat = geoloc.gimmie_loc(address=user.destiny.address,
                                     number=user.destiny.number,
                                     neighborhood=user.destiny.neighborhood,
                                     city=user.destiny.city,
                                     state=user.destiny.state)
        if lat == 404:
            print("Nominatim server error. Don't blame me...")
            freight = 0
            # lat = os.environ["SHOP_LAT"]
            # lon = os.environ["SHOP_LON"]
            # # lat, lon = (-23.5710819, -46.649922)  # seria as cordenadas da loja.
        else:
            print("Nominatim server is cool!")
            distance = geoloc.calculate_distance(lat, lon)
            freight = distance * 1.25
    else:
        freight = 0
    return freight


def organize_order_test(payment_dictionary):
    preferences = {"items": []}
    for key, value in payment_dictionary.items():
        preferences["items"].append(
            {"title": value["name"],
             "quantity": value["quantity"],
             "currence_id": "BRL",
             "unit_price": value["price"]})
    return preferences


@cart.route('/addcart', methods=['POST'])
def add_cart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method == "POST":
            dict_items = {product_id: {"name": product.name,
                                       "price": product.price,
                                       "quantity": quantity,
                                       "image": product.image}}
            if 'shopping_cart' in session:
                print(session['shopping_cart'])
                if product_id in session['shopping_cart']:
                    for key, item in session['shopping_cart'].items():
                        if int(key) == int(product_id):
                            print('lu-li-li-lo-lo')
                            print(session['shopping_cart'])
                            session.modified = True
                            print(item['quantity'])
                            item['quantity'] += 1
                    print("This product is already in your cart!")
                else:
                    session['shopping_cart'] = MagerDicts(session['shopping_cart'], dict_items)
                    return redirect(request.referrer)
            else:
                session['shopping_cart'] = dict_items
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@cart.route('/carts')
def get_cart():
    if 'shopping_cart' not in session or len(session['shopping_cart']) <= 0:
        flash('Seu carrinho está vazio! Por favor, coloque um produto.')
        return redirect(url_for('main.index'))
    sum_item_unit = 0
    subtotal = 0
    try:
        freight = calculate_freight()
    except Exception as e:
        freight = 0
        print(e)
    for key, product in session['shopping_cart'].items():
        subtotal += float(product['price'] * int(product['quantity']))
        grandtotal = subtotal + freight
        sum_item_unit += int(product['quantity'])
    return render_template('products/carts.html',
                           freight=freight,
                           subtotal=subtotal,
                           grandtotal=grandtotal,
                           sum_item_unit=sum_item_unit)


@cart.route('/updatecart/<int:code>', methods=['POST'])
def update_cart(code):
    print("banana split")
    if 'shopping_cart' not in session and len(session['shopping_cart']) <= 0:
        return redirect(url_for('main.index'))
    print('passou até aqui 1')
    if request.method == "POST":
        quantity = request.form.get('quantity')
        print('passou até aqui 2')
        try:
            session.modified = True
            for key, item in session['shopping_cart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('Seu carrinho foi atualizado!')
                    return redirect(url_for('cart.get_cart'))
        except Exception as e:
            print('Damn it!')
            print(e)
            redirect(url_for('cart.get_cart'))


@cart.route('/deleteitem/<int:id>')
def delete_item(id):
    if 'shopping_cart' not in session and len(session['shopping_cart']) <= 0:
        return redirect(url_for('main.index'))
    try:
        session.modified = True
        for key, item in session['shopping_cart'].items():
            if int(key) == id:
                session['shopping_cart'].pop(key, None)
                return redirect(url_for('cart.get_cart'))

    except Exception as e:
        print(e)
        return redirect(url_for('cart.get_cart'))


@cart.route('/emptycart')
def empty_cart():
    try:
        session.pop('shopping_cart', None)
        return redirect(url_for("main.index"))
    except Exception as e:
        print(e)


@cart.route('/buy')
def buy_product():
    cart_order = session['shopping_cart']
    try:
        freight_value = calculate_freight()
        session.pop('shopping_cart', None)
    except Exception as e:
        print(e)
    return redirect(Payment().payment(cart_order, freight_value))
