import json

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import DataRequired, NumberRange

import urllib.request
import json

class ClientDataForm(FlaskForm):

    age = IntegerField('Age', validators=[NumberRange(min=1, max=150)], default='42')
    gender = SelectField('Gender', coerce=str, choices=[('male', 'Male'), ('female', 'Female')], default='male')
    polyuria = SelectField('Polyuria', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    polydipsia = SelectField('Polydipsia', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    sudden_weight_loss = SelectField('Sudden weight loss', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    weakness = SelectField('Weakness', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    polyphagia = SelectField('Polyphagia', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    genital_thrush = SelectField('Genital thrush', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    visual_blurring = SelectField('Visual blurring', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    itching = SelectField('Itching', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    irritability = SelectField('Irritability', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    delayed_healing = SelectField('Delayed healing', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    partial_paresis = SelectField('Partial paresis', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')   
    muscle_stiffness = SelectField('Muscle stiffness', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    alopecia = SelectField('Alopecia', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    obesity = SelectField('Obesity', coerce=str, choices=[('no', 'No'), ('yes', 'Yes')], default='no')

app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)

def get_prediction(
    age, gender, polyuria,
    polydipsia, sudden_weight_loss, weakness,
    polyphagia, genital_thrush, visual_blurring, 
    itching, irritability, delayed_healing, 
    partial_paresis, muscle_stiffness, alopecia, 
    obesity
    ):
    body = {
        'age': age, 'gender': gender, 'polyuria': polyuria,
        'polydipsia': polydipsia, 'sudden_weight_loss': sudden_weight_loss, 'weakness': weakness,
        'polyphagia': polyphagia, 'genital_thrush': genital_thrush, 'visual_blurring': visual_blurring,
        'itching': itching, 'irritability': irritability, 'delayed_healing': delayed_healing,
        'partial_paresis': partial_paresis, 'muscle_stiffness': muscle_stiffness, 'alopecia': alopecia, 
        'obesity': obesity        
        }

    myurl = "http://0.0.0.0:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    #print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['age'] = request.form.get('age')
        data['gender'] = request.form.get('gender')
        data['polyuria'] = request.form.get('polyuria')
        data['polydipsia'] = request.form.get('polydipsia')
        data['sudden_weight_loss'] = request.form.get('sudden_weight_loss')
        data['weakness'] = request.form.get('weakness')
        data['polyphagia'] = request.form.get('polyphagia')
        data['genital_thrush'] = request.form.get('genital_thrush')
        data['visual_blurring'] = request.form.get('visual_blurring')
        data['itching'] = request.form.get('itching')
        data['irritability'] = request.form.get('irritability')
        data['delayed_healing'] = request.form.get('delayed_healing')
        data['partial_paresis'] = request.form.get('partial_paresis')
        data['muscle_stiffness'] = request.form.get('muscle_stiffness')
        data['alopecia'] = request.form.get('alopecia')
        data['obesity'] = request.form.get('obesity')
        
        try:
            response = str(get_prediction(
                data['age'], data['gender'], data['polyuria'],
                data['polydipsia'], data['sudden_weight_loss'], data['weakness'], 
                data['polyphagia'], data['genital_thrush'], data['visual_blurring'], 
                data['itching'], data['irritability'], data['delayed_healing'], 
                data['partial_paresis'], data['muscle_stiffness'], data['alopecia'], 
                data['obesity']
                ))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
