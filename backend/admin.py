from flask import Flask, request, json, jsonify, session, redirect, url_for
from flask_cors import CORS, cross_origin
from cas import CASClient
app = Flask(__name__)
c = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'

cas = CASClient(
	version = 3,
	service_url='https://127.0.0.1:5000/',
	server_url='https://cas.auth.rpi.edu/cas/'
	)


@app.route('/guard')
def guard(method=['GET']):
	if 'username' in session:
		return '{"auth": "1"}'
	else:
		return '{"auth": "0"}'

@app.route('/admin')
def index():
	return redirect(url_for('login'))

@app.route('/login', methods=["POST", "GET"])
def login():
	next = request.args.get('nxt')
	#print(next)
	ticket = request.args.get('ticket')
	if not ticket:
		print(cas.get_login_url())
		return redirect(cas.get_login_url())

	print(ticket)

	if not user:
		return "Failed to Verify Login Ticket"
	else:
		session['username'] = user
		return redirect(next)
	user, attributes, pgtiou = cas.verify_ticket(ticket)



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

if __name__ == '__main__':
	app.run(debug=True)
