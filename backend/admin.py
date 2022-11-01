from crypt import methods
from unicodedata import name
from flask import Flask, request, json, jsonify, session, redirect, url_for, render_template
from flask_cors import CORS, cross_origin
from cas import CASClient
import flask
flask.__version__
app = Flask(__name__)
c = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'

cas = CASClient(
        version = 3,
        service_url='https://ec2-52-90-250-109.compute-1.amazonaws.com/login/rpi',
        server_url='https://cas.auth.rpi.edu/cas/'
        )


@app.route('/guard')
def guard(method=['GET']):
        if 'username' in session:
                return jsonify('{"auth": "1"}')
        else:
                return jsonify('{"auth": "0"}')

@app.route('/admin')
def index():
        return redirect(url_for('login'))

@app.route('/login/rpi', methods=["POST", "GET"])
def login():
        #print(next)
        ticket = request.args.get('ticket')
        if not ticket:
                print(cas.get_login_url())
                return redirect(cas.get_login_url())

        print(ticket)
        user, attributes, pgtiou = cas.verify_ticket(ticket)

        if not user:
                return "Failed to Verify Login Ticket"
        else:
                session['username'] = user
                return redirect("https://hasspathways.com/admin-portal")



@app.route("/edit", methods=["POST", "GET"])
def editAdmin():
        response = {'status':'success'}
        if request.method == "POST":
                dat = request.get_json()
                name = dat.get('courses'),
                pathways = dat.get('pathways')
                print(name)
                print(pathways)

                response['message'] = 'Success!'

        return jsonify(response)

@app.route("/testing_year_courses", methods=["POST","GET"])
def host_year_courses_data():
        if request.method == "POST":               
                with open("data/" + request.args['year'] + "/courses.json", "r") as route:
                        
                        data= json.load(route)
                return  data

@app.route("/testing_year_pathways", methods=["POST","GET"])
def host_year_pathways_data():
        if request.method == "POST":
                with open("data/" + request.args['year'] + "/pathways.json", "r") as route:
                        data= json.load(route)
                return  data

@app.route("/testing_pathawys", methods=["GET"])
def host_pathways_data():
        with open("data/json/pathways_categories.json", "r") as route:
                data= json.load(route)
        return  data

@app.route("/testing_years", methods=["GET"])
def host_years_data():
        with open("data/json/years.json", "r") as route:
                data= json.load(route)
        return  data

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)