import subprocess
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
@app.route("/edit-course", methods=["POST", "GET"])
def editAdminCourse():
        response = {'status':'success'}
        if request.method == "POST":
                dat = request.get_json()

                with open('../frontend/src/data/json/' + dat['year'] + '/courses.json','r') as cs_file:
                        cs_data = json.load(cs_file)
                with open('../frontend/src/data/json/' + dat['year'] + '/pathways.json','r') as pw_file:
                        pw_data = json.load(pw_file)

                course_name = dat['course']['name']
                full_code = dat['course']['subj'] + dat['course']['ID']

                if dat['type'] == 'add':
                        cs_data[course_name] = dat['course']
                        for pw in dat['pathways']:
                                pw_data[pw]['Remaining'][course_name] = full_code

                elif dat['type'] == 'edit':
                        original_name = dat['original_course']['name']
                        if original_name != course_name:
                                dat.pop(original_name)
                        cs_data[course_name] = dat['course']
                        for pw in pw_data:
                                inside = False
                                for heading in pw_data[pw]:
                                        if original_name in pw_data[pw][heading]:
                                                inside = True
                                                pw_data[pw][heading].pop(original_name)
                                                pw_data[pw][heading][course_name] = full_code
                                if not inside and pw in dat['pathways']:
                                        pw_data[pw]['Remaining'][course_name] = full_code

                elif dat['type'] == 'remove':
                        cs_data.pop(course_name)
                        for pw in pw_data:
                                for heading in pw_data[pw]:
                                        if course_name in pw_data[pw][heading]:
                                                pw_data[pw][heading].pop(course_name)

                with open('../frontend/src/data/json/' + dat['year'] + '/courses.json','w') as cs_file:
                        json.dump(cs_data,cs_file,indent=2,ensure_ascii=False)
                with open('../frontend/src/data/json/' + dat['year'] + '/pathways.json','w') as pw_file:
                        json.dump(pw_data,pw_file,indent=2,ensure_ascii=False)

                subprocess.run(['./admin.sh',dat['year']])

                response['received'] = course_name
                response['message'] = 'Success!'
        return jsonify(response)

@app.route("/edit-pathway", methods=["POST", "GET"])
def editAdminPathway():
    response = {'status':'success'}
    if request.method == "POST":
            dat = request.get_json()

            with open('../frontend/src/data/json/' + dat['year'] + '/courses.json','r') as cs_file:
                    cs_data = json.load(cs_file)
            with open('../frontend/src/data/json/' + dat['year'] + '/pathways.json','r') as pw_file:
                    pw_data = json.load(pw_file)

            pathway_name = dat['pathway']['name']

            if dat['type'] == 'update':
                    for course in dat['courses']:
                            cs_data[course['name']] = course
                    pw_data[pathway_name] = dat['pathway']

            elif dat['type'] == 'remove':
                    for heading in pw_data[pathway_name]:
                            if dat['course']['name'] in pw_data[pathway_name][heading]:
                                    pw_data[pathway_name][heading].pop(dat['course']['name'])

            with open('../frontend/src/data/json/' + dat['year'] + '/courses.json','w') as cs_file:
                    json.dump(cs_data,cs_file,indent=2,ensure_ascii=False)
            with open('../frontend/src/data/json/' + dat['year'] + '/pathways.json','w') as pw_file:
                    json.dump(pw_data,pw_file,indent=2,ensure_ascii=False)

            subprocess.run(['./admin.sh',dat['year']])

            response['message'] = 'Success!'
    return jsonify(response)

if __name__ == '__main__':
        app.run(host='0.0.0.0')
