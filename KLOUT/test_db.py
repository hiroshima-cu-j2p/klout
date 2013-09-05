'''
Created on 2013/08/28

@author: naoya.fujii
'''
from app import db
from app.models import User, Vendor, Customer


def printUsers():
    print "======================"

    user_list  = db.session.query(User).all()
    for user in user_list:
        print user.type, user.nickname, user.user_name, user.e_mail, user.password
    
    print "======================"
    
    user_list  = db.session.query(Vendor).all()
    for user in user_list:
        print user.type, user.nickname, user.user_name, user.e_mail, user.password

    print "======================"

    user_list  = db.session.query(Customer).all()
    for user in user_list:
        print user.type, user.nickname, user.user_name, user.e_mail, user.password

    
u1 = User(id=1, nickname='U1', e_mail='u@e', user_name='u1', password='pass') 
db.session.add(u1)

v1 = Vendor(id=2, nickname='V1', e_mail='v@e', user_name='v1', password='pass')
db.session.add(v1)

c1 = Customer(id=3, nickname='C1', e_mail='c@e', user_name='c1', password='pass')
db.session.add(c1)

db.session.commit()

printUsers()