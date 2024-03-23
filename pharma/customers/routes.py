import secrets

from flask import render_template, session, request, redirect, url_for, flash
from pharma import app, db, bcrypt, login_manager
from flask_login import login_required,current_user,login_user,logout_user
from .form import CustomerRegisterForm , CustomerLoginForm
from.models import RegisterCustomer, CustomerOrder

# @app.route('/checkout')
# def checkout():
#     return render_template('products/checkout.html')

#

@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = RegisterCustomer(first_name=form.first_name.data, last_name=form.last_name.data,
                                    email=form.email.data,username=form.username.data,
                                    password=hash_password,country=form.country.data,state=form.state.data,
                                    city=form.city.data,  zipcode=form.zipcode.data,address=form.address.data )
        db.session.add(register)
        flash(f'Welcome {form.first_name.data} Thank you for registering','success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customer/customer_reg.html', form=form)


@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = RegisterCustomer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            #flash('You are login in now', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('incorrect email and password','danger')
        return redirect(url_for('customerLogin'))
    return render_template('customer/customer_login.html', form=form)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('customerLogin'))


@app.route('/checkout', methods=['GET','POST'])
@login_required
def checkout():
    user = RegisterCustomer.query.get_or_404(current_user.id)

    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    grandtotal = 0
    total_items = 0
    for key, product in session['Shoppingcart'].items():
        grandtotal += float(product['price']) * int(product['quantity'])
        total_items += int(product['quantity'])
    return render_template('customer/checkout.html', grandtotal=grandtotal,
                           total_items=total_items, user=user)

@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders= session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash("Your order has been sent", 'success')
            return redirect(url_for('allproduct'))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while getting order', 'danger')
            return redirect(url_for('checkout'))

@app.route('/cust_orders/<invoice>')
@login_required
def cust_orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = RegisterCustomer.query.filter_by(id=customer_id)
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).first()

        for _key, product in orders.orders.items():
            subTotal += float(product['price']) + int(product['quantity'])
        else:
            redirect(url_for('customerLogin'))
        return render_template('customer/cust_order.html', invoice=invoice,
                               subTotal=subTotal,customer=customer,orders=orders)