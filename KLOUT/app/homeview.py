'''
Created on 2013/08/29

@author: naoya.fujii
'''
from app import app, db
from app.models import Product_Category, Product, Classification, UserProduct,\
    User
from flask import render_template, request
from flask_login import current_user
from sqlalchemy.sql.expression import and_, func
from werkzeug.utils import redirect

def getCategories():
    return db.session.query(Product_Category).order_by(Product_Category.id).all()

@app.route("/selectproduct")
def selectproduct():
    categories = getCategories()
    products = db.session.query(Product).all()
    return render_template('Selectproduct.html', user=current_user, categories=categories,products=products)

@app.route("/searchProducts", methods=['POST'])
def searchProduct():
    category = request.form['category_id']
    product_name = request.form['product_name']
    products = db.session.query(Product).join(Classification, Classification.product_id==Product.id).filter(and_(
                                                                                                 Classification.category_id==category,
                                                                                                 Product.product_name.like('%{0}%'.format(product_name)))).all()
    return render_template("show_product.html", user=current_user, products=products)                                                                                                 

@app.route("/detail",methods=['POST'])
def detail():
    return render_template('detail.html')

@app.route("/create_new")
def create_new():
    categories = getCategories()
    return render_template('Create_new.html', categories=categories)

@app.route('/confirmcreatepage' ,methods=['POST'])
def confirmcreatepage():
    product_name = request.form['product_name']
    category_id = request.form['category_id']
    description= request.form['description']
    product_image = request.form['product_image']
    maximumId = db.session.query(func.max(Product.id)).scalar() # Get Max Product id
    if not maximumId: maximumId = 0 
    new_product_id=maximumId+1  # Set new product id as max product id + 1
    product = Product(id=new_product_id, product_name=product_name, 
                      description=description, product_image=product_image, 
                      want_count=0) # Create New Product Instance 
    
    maximumId = db.session.query(func.max(Classification.id)).scalar()  # Get Max Classification id
    if not maximumId: maximumId = 0
    new_classification_id=maximumId+1 # Set new Classification id as max Classification id + 1
    classification = Classification(id=new_classification_id, product_id=new_product_id, category_id=category_id)
    
    db.session.add(product) ## Insert into DB
    db.session.add(classification) ## Insert 
    db.session.commit() ## commit transaction
    
    category = db.session.query(Product_Category).filter(Product_Category.id==category_id).first()
    
    return render_template('Confirmcreatepage.html',product = product, category=category)

def get_highest_customer_price(product_id):
    customers = db.session.query(User).filter(User.type=='Customer').all()
    customer_ids = [customer.id for customer in customers]
    return db.session.query(func.max(UserProduct.price)).filter(and_(UserProduct.product_id==product_id,
                                                                     UserProduct.user_id.in_(customer_ids))).scalar()

def get_lowest_vendor_price(product_id):
    vendors = db.session.query(User).filter(User.type=='Vendor').all()
    vendor_ids = [vendor.id for vendor in vendors]
    return db.session.query(func.min(UserProduct.price)).filter(and_(UserProduct.product_id==product_id,
                                                                     UserProduct.user_id.in_(vendor_ids))).scalar()


def get_user_product(product_id):
    return db.session.query(UserProduct).filter(and_(
            UserProduct.user_id==current_user.id,
            UserProduct.product_id==product_id)).first()

@app.route("/detail_for_vendor")
def detail_for_vendor():
    #want_count =request.form.get('want_count', None)
    product_id = request.args['product_id']
    product = db.session.query(Product).filter(Product.id==product_id).first()
    
    user_product = db.session.query(UserProduct).filter(and_(
            UserProduct.user_id==current_user.id,
            UserProduct.product_id==product_id)).first()
    
    return  render_template('detail_for_vendor.html', product=product, 
                            user_product=user_product,
                            Vender_Lowest_Price=get_lowest_vendor_price(product_id),
                            Customer_Highest_Price=get_highest_customer_price(product_id))


@app.route("/detail_for_customer")
def detail_for_customer():
    #want_count =request.form.get('want_count', None)
    product_id = request.args['product_id']
    product = db.session.query(Product).filter(Product.id==product_id).first()
    
    user_product = get_user_product(product_id)
    
    return  render_template('detail_for_customer.html', product=product, 
                            user_product=user_product,
                            Vender_Lowest_Price=get_lowest_vendor_price(product_id),
                            Customer_Highest_Price=get_highest_customer_price(product_id))

def get_product(product_id):
    return db.session.query(Product).filter(Product.id==product_id).first()

@app.route("/saveCustomerChoice", methods=['POST'])
def saveCustomerChoice():
    product_id = request.form.get('product_id', None)
    user_product = get_user_product(product_id)
    product = get_product(product_id)
    if not user_product:
        maximumId = db.session.query(func.max(UserProduct.id)).scalar()  # Get Max UserProduct id
        if not maximumId: maximumId = 0
        new_user_product_id=maximumId+1 # Set new UserProduct id as max UserProduct id + 1
        user_product = UserProduct(id=new_user_product_id, 
                                   user_id=current_user.id, product_id=product_id,
                                   price = request.form['your_asking_price'], 
                                   want='Yes')
        product.want_count += 1
        db.session.add(product) # Update Want count on Product
    else:
        user_product.price = request.form['your_asking_price']
    
    db.session.add(user_product) ## Insert or Update into db
    db.session.commit() ## commit transaction
    return redirect("/detail_for_customer?product_id={0}".format(product_id))

@app.route("/saveVendorChoice", methods=['POST'])
def saveVendorChoice():
    product_id = request.form.get('product_id', None)
    user_product = get_user_product(product_id)
    if not user_product:
        maximumId = db.session.query(func.max(UserProduct.id)).scalar()  # Get Max UserProduct id
        if not maximumId: maximumId = 0
        new_user_product_id=maximumId+1 # Set new UserProduct id as max UserProduct id + 1
        user_product = UserProduct(id=new_user_product_id, 
                                   user_id=current_user.id, product_id=product_id,
                                   price = request.form['your_asking_price'], 
                                   want='Yes')
    else:
        user_product.price = request.form['your_asking_price']
    
    db.session.add(user_product) ## Insert or Update into db
    db.session.commit() ## commit transaction
    return redirect("/detail_for_vendor?product_id={0}".format(product_id))


# @app.route("/detail_for_vendor")
# def detail_for_vendor():
#     #want_count =request.form.get('want_count', None)
#     product_id = request.args['product_id']
#     product = db.session.query(Product).filter(Product.id==product_id).first()
#     return  render_template('detail_for_vendor.html', product=product, Vender_Lowest_Price=10000,Customer_Highest_Price=8000,
#                             YOUR_SELECT_PRICE=9000,vendor_name='a',vendor_price=5000)


@app.route("/purchaser_page")
def purchaser_page():
    return render_template('purchaser_page.html')
    
@app.route("/finish_purchase")
def finish_purchase():
    return render_template('finish_purchase.html')