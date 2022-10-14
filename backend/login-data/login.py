from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from passlib.context import CryptContext

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Credentials.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(1024))
    last = db.Column(db.String(1024))
    email = db.Column(db.String(1024), unique=True)
    password = db.Column(db.String(1024), unique=True)

# Entry(id=1, first='Nick', last='Dicosimo', email='asbasf@gasd.com', password='sadfsadf')

def hash(str: password):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)

def dehash(str: password, hash):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(password, hash)
#how to write a route for flask
@app.route(methods = ["GET", "POST"])
def requests():
    if request.method=="POST":
        first_got = request.form["first"]
        # request.form.get('first')

    #Entry.query.filter_by(email=email_got).first() <search database
        return "STRING"

    #some variable = Entry() <- args should be (first=first_got ... )

    #commit to the database
    db.session #.add() <- add entry object
    db.session #.commit()

@app.route(methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        #get username
        #get password
        
        check = #Entry.query.filter_by(email=email_got).first()
        #search database for username


        #if and verify the password is correct
