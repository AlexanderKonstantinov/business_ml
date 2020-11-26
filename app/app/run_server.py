# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py

# import the necessary packages
import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)
	print(model)

modelpath = "/app/app/models/cat_boost_classifier.dill"
load_model(modelpath)

@app.route("/", methods=["GET"])
def general():
	return """Welcome to early stage diabetes risk prediction process. Please use 'http://<address>/predict' to POST"""

@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")
	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":

		age = 42
		gender = 'male'
		polyuria, polydipsia, sudden_weight_loss = 'no', 'no', 'no' 
		weakness, polyphagia, genital_thrush = 'no', 'no', 'no' 
		visual_blurring, itching, irritability = 'no', 'no', 'no'
		delayed_healing, partial_paresis, muscle_stiffness = 'no', 'no', 'no'
		alopecia, obesity = 'no', 'no'

		request_json = flask.request.get_json()
		if request_json["age"]:
			age = int(request_json['age'])
		if request_json["gender"]:
			gender = request_json['gender']
		if request_json["polyuria"]:
			polyuria = request_json['polyuria']
		if request_json["polydipsia"]:
			polydipsia = request_json['polydipsia']
		if request_json["sudden_weight_loss"]:
			sudden_weight_loss = request_json['sudden_weight_loss']
		if request_json["weakness"]:
			weakness = request_json['weakness']
		if request_json["polyphagia"]:
			polyphagia = request_json['polyphagia']
		if request_json["genital_thrush"]:
			genital_thrush = request_json['genital_thrush']
		if request_json["visual_blurring"]:
			visual_blurring = request_json['visual_blurring']
		if request_json["itching"]:
			itching = request_json['itching']
		if request_json["irritability"]:
			irritability = request_json['irritability']
		if request_json["delayed_healing"]:
			delayed_healing = request_json['delayed_healing']
		if request_json["partial_paresis"]:
			partial_paresis = request_json['partial_paresis']
		if request_json["muscle_stiffness"]:
			muscle_stiffness = request_json['muscle_stiffness']
		if request_json["alopecia"]:
			alopecia = request_json['alopecia']
		if request_json["obesity"]:
			obesity = request_json['obesity']		

		logger.info(f'''{dt} Data: 
age={age}, gender={gender}, polyuria={polyuria}, 
polydipsia={polydipsia}, sudden_weight_loss={sudden_weight_loss}, weakness={weakness}, 
polyphagia={polyphagia}, genital_thrush={genital_thrush}, visual_blurring={visual_blurring}, 
itching={itching}, irritability={irritability}, delayed_healing={delayed_healing}, 
partial_paresis={partial_paresis}, muscle_stiffness={muscle_stiffness}, alopecia={alopecia}, 
obesity={obesity}
''')
		try:
			preds = model.predict_proba(pd.DataFrame({
				"Age": [age], "Gender": [gender], "Polyuria": [polyuria],
				"Polydipsia": [polydipsia], "sudden weight loss": [sudden_weight_loss], "weakness": [weakness],
				"Polyphagia": [polyphagia], "Genital thrush": [genital_thrush], "visual blurring": [visual_blurring],
				"Itching": [itching], "Irritability": [irritability], "delayed healing": [delayed_healing],
				"partial paresis": [partial_paresis], "muscle stiffness": [muscle_stiffness], "Alopecia": [alopecia],
				"Obesity": [obesity]
				}))
		except AttributeError as e:
			logger.warning(f'{dt} Exception: {str(e)}')
			data['predictions'] = str(e)
			data['success'] = False
			return flask.jsonify(data)

		data["predictions"] = preds[:, 1][0]
		# indicate that the request was a success
		data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 8180))
	app.run(host='0.0.0.0', debug=True, port=port)
