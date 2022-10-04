from flask import Flask, request, json, jsonify, session, redirect, url_for
from flask_cors import CORS, cross_origin
app = Flask(__name__)
c = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'
#
# cas = CASClient(
#         version = 3,
#         service_url='https://ec2-52-90-250-109.compute-1.amazonaws.com/login/rpi',
#         server_url='https://cas.auth.rpi.edu/cas/'
#         )
#

# @app.route('/guard')
# def guard(method=['GET']):
#         if 'username' in session:
#                 return jsonify('{"auth": "1"}')
#         else:
#                 return jsonify('{"auth": "0"}')
#
# @app.route('/admin')
# def index():
#         return redirect(url_for('login'))
#
# @app.route('/login/rpi', methods=["POST", "GET"])
# def login():
#         #print(next)
#         ticket = request.args.get('ticket')
#         if not ticket:
#                 print(cas.get_login_url())
#                 return redirect(cas.get_login_url())
#
#         print(ticket)
#         user, attributes, pgtiou = cas.verify_ticket(ticket)
#
#         if not user:
#                 return "Failed to Verify Login Ticket"
#         else:
#                 session['username'] = user
#                 return redirect("https://hasspathways.com/admin-portal")
#
#
#
@app.route("/edit", methods=["POST", "GET"])
def editAdmin():
        response = {'status':'success'}
        if request.method == "POST":
                dat = request.get_json()

                with open('../frontend/src/data/json/' + dat['year'] + '/courses.json','r') as cs_file:
                        cs_data = json.load(cs_file)
                with open('../frontend/src/data/json/' + dat['year'] + '/pathways.json','r') as pw_file:
                        pw_data = json.load(pw_file)
                course_name = dat['courses']['name']

                if dat.get('type') == 'add':
                        cs_data[course_name] = dat['courses']
                        full_code = dat['courses']['subj'] + dat['courses']['ID']
                        for pw in dat['pathways']:
                            pw_data[pw]['Remaining'] = full_code

                with open('../frontend/src/data/json/' + dat['year'] + '/courses.json','w') as cs_file:
                        json.dump(cs_data,cs_file,indent=2)
                with open('../frontend/src/data/json/' + dat['year'] + '/pathways.json','w') as pw_file:
                        json.dump(pw_data,pw_file,indent=2)

                os.execl('./admin.sh',dat['year'])

                response['received'] = course_name
                response['message'] = 'Success!'
        return jsonify(response)

if __name__ == '__main__':
        app.run(host='0.0.0.0')
