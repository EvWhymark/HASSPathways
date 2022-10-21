from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from passlib.context import CryptContext

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Credentials.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

#this is a row
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(1024))
    last = db.Column(db.String(1024))
    email = db.Column(db.String(1024), unique=True)
    password = db.Column(db.String(1024))

# Entry(id=1, first='Nick', last='Dicosimo', email='asbasf@gasd.com', password='sadfsadf')

def hash(password):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)

def checkhash(password, hash):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(password, hash)
#how to write a route for flask
#THIS IS FOR ACCOUNT CREATION
@app.route('/register',methods = ["GET", "POST"])   #what is this one for? Post/Get? Post = send data to fnction, Get = give data to client
def requests():
    if request.method=="POST":
        first_got = request.args["first"]
        last_got = request.args["last"]
        email_got = request.args["email"]
        if Entry.query.filter_by(email=email_got).first(): #<search database
            return "failure"
        password_got = hash(request.args["password"]) #----- do I hash or dehash here


        newEntry = Entry(first=first_got, last=last_got, email=email_got, password = password_got) #<- args should be (first=first_got ... )

        #commit to the database
        db.session.add(newEntry) #<- add entry object
        db.session.commit()
        return "success"
#THIS ONE IS FOR LOGGING
@app.route('/login',methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        email_got = request.args["email"]
        if not Entry.query.filter_by(email=email_got):
            return "Email not in the database"
        if checkhash(hash(request.args["password"]),Entry.query.get(email_got).password):
            return "Success"
        else:
            return "Failure"



if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
