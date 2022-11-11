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

#opens courses.json file based on a certain year range
@app.route("/testing_year_courses", methods=["POST"])
def host_year_courses_data():
        if request.method == "POST":         
                with open("data/json/years.json", "r") as route:
                        data = json.load(route)
                        if request.args['year'] not in data:
                                year = request.args['year']
                                return render_template("year_endpoint.html", year = year)         
                with open("data/json/" + request.args['year'] + "/courses.json", "r") as route:
                        data = json.load(route)   
                return  data            

#opens pathways.json file based on a certain year range
@app.route("/testing_year_pathways", methods=["POST"])
def host_year_pathways_data():
        if request.method == "POST":
                with open("data/json/years.json", "r") as route:
                        data = json.load(route)
                        if request.args['year'] not in data:
                                year = request.args['year']
                                return render_template("year_endpoint.html", year = year)  
                with open("data/json/" + request.args['year'] + "/pathways.json", "r") as route:
                        data = json.load(route)
                return  data
 # html template that just says this is a post endpoint, requires arg "year"
        
#open pathway_categories json file and converts it into a python dictionary
@app.route("/testing_pathawy_categories")
def host_pathways_data():
        with open("data/json/pathway_categories.json", "r") as route:
                data = json.load(route)
        return  data

#open years.json file and converts it into a python dictionary
@app.route("/testing_years")
def host_years_data():
        with open("data/json/years.json", "r") as route:
                data = json.load(route)
        return  data

#open courses.json file and converts it into a python dictionary
@app.route("/testing_JSON_FILES_courses")
def host_jsonfile_courses():
        with open("../JSONfiles/courses.json", "r") as route:
                data = json.load(route)
        return  data

#open pathways.json file and converts it into a python dictionary
@app.route("/testing_JSON_FILES_pathways")
def host_jsonfile_pathways():
        with open("../JSONfiles/pathways.json", "r") as route:
                data = json.load(route)
        return  data 

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

# refining:
#       - currently accepting post and get -- bad done done
#       - comment your code done done
#       - make sure year given is in years.json done
#       - add year endpoint 
#            - save that new data (should accept same files pathway.json ...) to a new folder amptly named after the year that was passed
#              as another argument
#            - attach a private key to this
#               - protect it
#            - second endpoint
#               - set passkey (default passkey is something)
#                       - former pass key, make sure it is equal to current, then change
#                       - hash the passkey using cryptcontext (.hash() .verify())   .ppk .pem
