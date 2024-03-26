from flask import render_template, session, request, redirect, url_for, flash

from pharma import db, app, search
from .models import Category, Addproduct
from .forms import Addproducts

import secrets
import os


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images1', picture_fn)

    form_picture.save(picture_path)

    return picture_fn



@app.route('/home')
@app.route("/")
def home():

    return render_template('products/index.html')


@app.route('/allproduct')
def allproduct():
    page = request.args.get('page',1,type=int)
    products = Addproduct.query.paginate(page=page, per_page=12)
    return render_template('products/allproduct.html', title='All Products'
                           ,products=products)

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name','desc'], limit=6)
    return render_template('products/result.html', products=products)

@app.route('/market')
def market():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter_by(category_id=2).paginate(page=page, per_page=12)
    return render_template('products/market.html', products=products)



@app.route('/order')
def order():
    return render_template('products/order.html')


@app.route('/health')
def health():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter_by(category_id=1).paginate(page=page, per_page=12)
    return render_template('products/health.html', products=products)


@app.route('/beauty')
def beauty():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter_by(category_id=3).paginate(page=page, per_page=12)
    return render_template('products/beauty.html', products=products)



@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash("Please login first", 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getcat = request.form.get('cat')
        cat = Category(name=getcat)
        db.session.add(cat)
        flash(f"The Category {getcat} was added to you database", 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addcat.html', tittle='Add-Cat')


@app.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash("Please login first", 'danger')

    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecat.name = category
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('product/updatecat.html', title='UPDATE CATEGORY', updatecat=updatecat)

@app.route('/Addproduct', methods=['POST','GET'])
def addproduct():
    if 'email' not in session:
        flash("Please login first", 'danger')
        return redirect(url_for('login'))
    categories = Category.query.all()
    form = Addproducts()
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        print(stock)
        desc = form.description.data
        cat = request.form.get('category')
        image = form.image.data
        print(image)
        if image:
            picture_file = save_picture(form.image.data)
            addpro = Addproduct(name=name, price=price, stock=stock,desc=desc, category_id=cat, image=picture_file)
            db.session.add(addpro)

            flash(f"The product {name} has been added to your database ", 'success')
            db.session.commit()
            return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title='Add Products',form=form, categories=categories)


@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    product = Addproduct.query.get_or_404(id)
    categories = Category.query.all()
    category = request.form.get('category')
    form = Addproducts()
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.desc = form.description.data
        product.category_id = category
        db.session.commit()
        flash(f'Your product has been updated','success')
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.stock.data = product.stock
    form.description.data = product.desc
    return render_template('products/updateproduct.html', form=form, categories=categories, product=product)

@app.route('/deleteproduct<int:id>', methods=['GET', 'POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} has been deleted from your records', 'success')
        return redirect(url_for('admin'))
    flash(f'Cant delete the product', 'danger')
    return redirect(url_for('admin'))


@app.route('/item/<int:id>')
def item(id):
    product = Addproduct.query.get_or_404(id)
    cat_id = product.category_id
    random_products = Addproduct.query.filter_by(category_id=cat_id).order_by(db.func.random()).limit(5).all()

    return render_template('products/item.html', product=product,
                           random_products=random_products)


