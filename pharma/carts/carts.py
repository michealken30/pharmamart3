from flask import render_template, session, request, redirect, url_for, flash

from pharma import db, app
from pharma.products.models import Addproduct


def MegerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/addcart', methods=['GET', 'POST'])
def AddCart():
    try:
        if request.method == "POST":
            product_id = (request.form.get('product_id'))
            quantity = int(request.form.get('quantity'))
            product = Addproduct.query.filter_by(id=product_id).first()  # Added parentheses

            if product_id and quantity:
                DictItems = {
                    product_id: {
                        'name': product.name,
                        'price': product.price,
                        'quantity': quantity,
                        'image': product.image
                    }
                }

                if 'Shoppingcart' in session:

                    if product_id in session['Shoppingcart']:
                        session.modified = True
                        session['Shoppingcart'][product_id]['quantity'] += quantity

                    else:
                        session['Shoppingcart'] = MegerDicts(session['Shoppingcart'], DictItems)
                        return redirect(request.referrer)
                else:
                    session['Shoppingcart'] = DictItems
                    return redirect(request.referrer)  # Added return
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/cart')
def getcart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    grandtotal = 0
    total_items = 0
    for key, product in session['Shoppingcart'].items():
        grandtotal += float(product['price']) * int(product['quantity'])
        total_items += int(product['quantity'])
    return render_template('products/cart.html', grandtotal=grandtotal, total_items=total_items)


@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    try:
        # Check if 'Shoppingcart' key exists in session
        if 'Shoppingcart' not in session:
            return redirect(url_for('home'))

        if request.method == 'POST':
            quantity = int(request.form.get('quantity'))  # Convert quantity to integer

            # Loop through items in the shopping cart
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    # Update quantity if item code matches
                    item['quantity'] = quantity
                    session.modified = True  # Mark session as modified
                    flash('Item is updated', 'success')
                    return redirect(url_for('getcart'))

        # If no matching item is found
        flash('Item not found in the cart')
        return redirect(url_for('getcart'))

    except Exception as e:
        print(e)
        flash('Error updating item')
        return redirect(url_for('getcart'))


@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(request.args.get('return_url', '/cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getcart'))



@app.route('/clearcat')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('allproduct'))
    except Exception as e:
        print(e)
