import secrets
import pdfkit

from flask import render_template, session, request, redirect, url_for, flash, make_response
from pharma import app, db, bcrypt, login_manager
from flask_login import login_required, current_user, login_user, logout_user
from .form import CustomerRegisterForm, CustomerLoginForm
from.models import RegisterCustomer, CustomerOrder
import stripe

publishable_key = 'pk_test_51OxWPq02FNxgPW4uy85jCIUlQRQyCX6FUOdwft1WvEuFwKllopJV4fYOX74t7dn4yiOvTNVzJHWqkVnm29kIMRP600lPrwd1Lb'

stripe.api_key = 'sk_test_51OxWPq02FNxgPW4uJ8CuqZRF0MUzMJtaepViCCmsDwDOTMa8rLhkUhol68J8A0LFBAntBQR1ZOE6m1lVPbkOZU7A00HsMHsGzz'

@app.route('/payment', methods=['POST'])
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    amount = str(amount)
    print(amount)
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Myshop',
        amount=int(float(amount)),
        currency='usd',
    )
    orders = (CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).
              order_by(CustomerOrder.id.desc()).first())
    orders.status = 'Paid'
    db.session.commit()
    return redirect(url_for('thanks'))

@app.route('/thanks')
def thanks():
    return render_template('customer/thank.html')


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
        #flash(f'Welcome {form.first_name.data} Thank you for registering','success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
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


def updateshoppingcart():
    for key, product in session['Shoppingcart'].items():
        session.modified = True
        del product['image']

    return updateshoppingcart

@app.route('/getorder', methods=['GET', 'POST'])
@login_required
def get_order():

    if request.method == "POST":
        value = request.form.get('delivery-option-2')


        if current_user.is_authenticated:
            customer_id = current_user.id
            invoice = secrets.token_hex(5)
            updateshoppingcart()
            try:
                order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders= session['Shoppingcart'])
                db.session.add(order)
                db.session.commit()
                session.pop('Shoppingcart')
                #flash("Your order has been sent", 'success')
                return redirect(url_for('cust_orders', invoice=invoice, value=value))
            except Exception as e:
                print(e)
                #flash('Some thing went wrong while getting order', 'danger')
                return redirect(url_for('allproduct'))


@app.route('/get_pdf/<invoice>/<value>', methods=['GET', 'POST'])
@login_required
def get_pdf(invoice, value):


    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id


        if request.method == 'POST':
            customer = RegisterCustomer.query.get(customer_id)
            orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()

            for product in orders.orders.values():
                subTotal += float(product['price']) * int(product['quantity'])
                grandTotal = subTotal + int(value)

            rendered = render_template('customer/pdf.html', invoice=invoice,
                                   grandTotal=grandTotal, customer=customer, orders=orders, value=value)

            path_wkthmltopdf = b'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

            pdf = pdfkit.from_string(rendered, False, configuration=config)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'atteched; filename='+invoice+'.pdf'
            return response
    return redirect(url_for('cust_orders'))


@app.route('/cust_orders/<invoice>/<value>', methods=['GET', 'POST'])
@login_required
def cust_orders(invoice, value):


    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        print(value)

        # Assuming 'RegisterCustomer' and 'CustomerOrder' are your SQLAlchemy models
        customer = RegisterCustomer.query.get(customer_id)
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()

        for product in orders.orders.values():
            subTotal += float(product['price']) * int(product['quantity'])
            grandTotal = subTotal + int(value)


        return render_template('customer/cust_order.html', invoice=invoice,
                               grandTotal=grandTotal, customer=customer, orders=orders, value=value)
    else:
        return redirect(url_for('customerLogin'))

