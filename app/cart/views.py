from flask import redirect, render_template, url_for, flash, request, session,\
    current_app
from . import cart
from ..models import Product

def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@cart.route('/addcart', methods=['POST'])
def add_cart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method == "POST":
            Dict_items = {product_id:{'name': product.name,
                                     "price": product.price,
                                     "quantity": quantity,
                                     "image": product.image}}
            if 'shopping_cart' in session:
                print(session['shopping_cart'])
                if product_id in session['shopping_cart']:
                    print("This product is already in your cart!")
                else:
                    session['shopping_cart'] = MagerDicts(session['shopping_cart'], Dict_items)
                    return redirect(request.referrer)
            else:
                session['shopping_cart'] = Dict_items
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

