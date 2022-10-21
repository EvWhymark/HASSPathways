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

def dehash(password, hash):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(password, hash)
#how to write a route for flask
@app.route('/ajfoao',methods = ["GET", "POST"])
def requests():
    if request.method=="POST":
        first_got = request.args["first"]
        # request.form.get('first')

    #if Entry.query.filter_by(email=email_got).first(): <search database
        return first_got

    #some variable = Entry(first=first_got, username=...) <- args should be (first=first_got ... )

    #commit to the database
    # db.session.add(Entry) <- add entry object
    # db.session #.commit()

@app.route('/ggggggg',methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        #get username
        #get password
        
        #check = #Entry.query.filter_by(email=email_got).first()
        #search database for username

        return 'yes'
        #if and verify the password is correct


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
