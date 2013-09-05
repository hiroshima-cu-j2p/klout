'''
Created on 2013/08/28

@author: naoya.fujii
'''
from app import app, db, login_manager
from app.models import User, check_user_and_password, Customer, Vendor,Product,UserProduct,check_e_mail_and_password
from flask import render_template, request
from flask.helpers import flash, url_for
from flask_login import login_user, login_required, logout_user,current_user
from sqlalchemy.sql.expression import and_,func
from werkzeug.utils import redirect


@app.route("/")
def hello():
    return render_template('loginpage.html')

@app.route('/formPage')
def formPage():
    return render_template('formpage.html')

@app.route('/formSubmit',methods=['POST'])
def formSubmit():
    username = request.form['username']
    email = request.form['email']
    nickname = request.form['nickname']
    password = request.form['password']
    com_pass = request.form['confirm_password']
    user_type = request.form['user_type']
    
    error = None
    if username == '' :
        error = 'Please provide the username!'
    elif email == '':
        error = 'Please provide the email!'
    elif nickname == '':
        error = 'Please provide the nickname!'
    elif password == '':
        error = 'Please provide the password!'
    elif com_pass == '':
        error = 'Please provide the confirm password!'
    elif len(password) < 4 or len(password) > 8:
        error = 'Password of your choice is wrong!'
        
    elif password != com_pass:
        error = 'Password is not same "CONFIRM PASSWORD"!'
    elif '@' not in email:
        error = 'Your e-mail address is wrong!'
    elif user_type != 'Customer' and user_type != 'Vendor':
        error = "Please choose correct user type" 
    
    if error:
        return render_template('formPage.html', message=error)
    else:
        from app.models import User
        maximumId = db.session.query(func.max(User.id)).scalar()
        if not maximumId: maximumId = 0
        if user_type == 'Customer':
            user = Customer(id=maximumId+1, user_name=request.form['username'], 
                        e_mail=request.form['email'],
                        nickname=request.form['nickname'],
                        password=request.form['password'])
        elif user_type == 'Vendor':
            user = Vendor(id=maximumId+1, user_name=request.form['username'], 
                        e_mail=request.form['email'],
                        nickname=request.form['nickname'],
                        password=request.form['password'])
        
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return render_template('confirmpage.html', id=maximumId+1, username=username,email=email,nickname=nickname,user_type=user_type)
        
@login_manager.user_loader
def load_user(userid):
    return db.session.query(User).filter(User.id==userid).first() 

@app.route('/loginpage', methods=['GET','POST'])
def loginpage():
    login_username = request.form['login_username']
    login_e_mail = request.form['login_e_mail']
    login_password = request.form['login_password']
    user = check_user_and_password(login_username, login_password)
    if not user:
        user1 = check_e_mail_and_password(login_e_mail, login_password)
        if not user1:    
            flash("Incorrect User Name Password")
            return redirect("/")
        else:
            login_user(user1)
            return redirect("/selectproduct")
    else :
        login_user(user)
        return redirect("/selectproduct")

@app.route("/settings")
@login_required
def settings():
    pass

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

