'''
Created on 2013/08/28

@author: naoya.fujii
'''
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    e_mail = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(8), nullable=False)
    created_on = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(8), nullable=False)
    
    __mapper_args__= {
                       'polymorphic_on':type,
                       'polymorphic_identity':'User'
                      }

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id

class Vendor(User):
    __mapper_args__= { 'polymorphic_identity':'Vendor' }
    
class Customer(User):
    __mapper_args__= { 'polymorphic_identity':'Customer' }
    
    
def check_user_and_password(username, password):
    user = db.session.query(User).filter(User.user_name==username,
                                         User.password==password).first()
    return user

def check_e_mail_and_password(e_mail, password):
    user1 = db.session.query(User).filter(User.e_mail==e_mail,
                                         User.password==password).first()
    return user1
  
class Product_Category(db.Model):
    __tablename__ = 'p_categories'
    
    id = db.Column(db.Integer,primary_key=True)
    category_name = db.Column(db.String(100),nullable=False)
    
    def __repr__(self):
        return "Id: {0}, Name:{1}".format(self.id, self.category_name)
    
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(255),nullable=False)
    created_on = db.Column(db.Date,nullable=False)
    want_count =db.Column(db.Integer,nullable=False)
    product_image =db.Column(db.String(255),nullable=False)

    def __repr__(self):
        return "Id: {0}, Name:{1}, description:{2}".format(self.id, self.name,self.description)
    
class Classification(db.Model):
    __tablename__ = 'classification'
    
    id = db.Column(db.Integer,primary_key=True)
    product_id = db.Column(db.Integer,nullable=False)
    category_id = db.Column(db.Integer,nullable=False)
  
class UserProduct(db.Model):
	__tablename__ = 'user_products'
	
	id = db.Column(db.Integer,primary_key=True)
	product_id = db.Column(db.Integer,nullable=False)
	user_id = db.Column(db.Integer,nullable=False)
	comments = db.Column(db.String(255))
	price = db.Column(db.Integer(11))
	quantity = db.Column(db.Integer(11))
	want = db.Column(db.String(3),nullable=False,default='No')
    
#class Shopper(db.Model):
#    __tablename__ = 'shopper'
#   
#    user_Id = db.Column(db.Integer,primary_key=True)# primary_key=True -> no error,primary_key=False -> error  but i want to no use primary_key
#   product_Id = db.Column(db.Integer,nullable=False)
#    category_Id = db.Column(db.Integer,nullable=False)
