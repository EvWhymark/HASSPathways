from flask import Flask, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from passlib.context import CryptContext
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage
login_app = Blueprint('login_app', __name__)
login_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Credentials.sqlite"
login_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_app.config["SECRET_KEY"] = 'apple'#change this
db = SQLAlchemy()
db.init_app(login_app)
#this is a row
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(1024))
    last = db.Column(db.String(1024))
    email = db.Column(db.String(1024), unique=True)
    password = db.Column(db.String(1024))

# Entry(id=1, first='Big', last='Dinkus', email='asbasf@gasd.com', password='sadfsadf')

def hash(password):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)

def checkhash(password, hash):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(password, hash)
#how to write a route for flask
#THIS IS FOR ACCOUNT CREATION
@login_app.route('/register',methods = ["GET", "POST"])   #what is this one for? Post/Get? Post = send data to fnction, Get = give data to client
def requests():
    if request.method=="POST":
        first_got = request.args["first"]
        last_got = request.args["last"]
        email_got = request.args["email"]
        if Entry.query.filter_by(email=email_got).first(): #<search database
            return "failure"

        newEntry = Entry(first=first_got, last=last_got, email=email_got, password = hash(request.args["password"])) #<- args should be (first=first_got ... )
        db.session.add(newEntry)
        db.session.commit()
        return "success"
#THIS ONE IS FOR LOGGING
@login_app.route('/login',methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
                    # if logged in sucess, if password was wrong (flash a message), usernme = if username exists
        response = {'loggedin':0, 'passwrd': 0, 'usernme': 0}
        email_got = request.form.get("email")
        if not Entry.query.filter_by(email=email_got):
            reponse['usernme'] = 1
        elif checkhash(hash(request.form.get("password")),Entry.query.get(email_got).password):
            response['loggedin'] = 1
        else:
            response['passwrd'] = 1
        return response

#maybe store censored email for multiple attempts? Nah you have to login w/ email so there's no point in sending a censored one
#@app.route('/reset_pass1',methods = ["GET", "POST"])
#def censored_email():
#    if request.method == 'POST':
#        email_got =

#maybe reset password?
@login_app.route('/change_password', methods = ["GET", "POST"]) #what is this one for? Post/Get? Post = send data to fnction, Get = give data to client
def reset_password():
    if request.method == 'POST':
        email_got = request.args["email"]
        if Entry.query.filter_by(email=email_got).first(): #<search database
            return "failure"
        password_got = hash(request.args["password"])
        Entry.query.get(email_got).password = password_got
        return "success"
    #if request.method == 'GET':
        #rand is good

    #how to sennd passwod
    #generate unique number, store it somewhere(local) json file: key: name, code check if code same

@login_app.route('/reset_password', methods = ["GET", "POST"]) #what is this one for? Post/Get? Post = send data to fnction, Get = give data to client
def change_password():
    if request.method == 'POST':
        email_got == request.args["email"]

           #rand is good

    #how to sennd passwod
    #generate unique number, store it somewhere(local) json file: key: name, code check if code same

#change personal info?
@login_app.route('/change_info')
def change_info():
    if request.method == 'POST':
        old_email_got = request.args["old_email"]
        if Entry.query.filter_by(email=old_email_got).first(): #<search database
            return "failure"
        first_got = request.args["first"]
        last_got = request.args["last"]
        new_email_got = request.args["new_email"]
        Entry.query.get(old_email_got).first = first_got
        Entry.query.get(old_email_got).last = last_got
        Entry.query.get(old_email_got).email = new_email_got
        return "success"