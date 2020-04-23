from flask import Flask, request, jsonify, render_template, flash
from flask.logging import create_logger
import logging
from wtforms import Form, TextField, validators
import pandas as pd
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
import json

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

def scale(payload):
    """Scales Payload"""
    
    LOG.info(f"Scaling Payload: \n{payload}")
    scaler = StandardScaler().fit(payload.astype(float))
    scaled_adhoc_predict = scaler.transform(payload.astype(float))
    return scaled_adhoc_predict

# @app.route("/")
# def home():
#     html = f"<h3>Sklearn Prediction Home</h3>"
#     return html.format(format)

class ReusableForm(Form):
    input = TextField('Input:', validators=[validators.DataRequired()])
    
@app.route("/", methods=['GET', 'POST'])
def home():
    form = ReusableForm(request.form)
    print(form.errors)
    
    if request.method == 'POST':
        input = request.form['input']

    if form.validate():
        try:
            json_prediction = json.loads(input)
            prediction = predict(json_prediction)
            print(prediction.data)
            flash(str(prediction.data.decode("utf-8") ))
        except json.decoder.JSONDecodeError:
            flash("Error: {} not a valid json".format(input))
        except ValueError:
            flash("Error: {} json not suited for this prediction script".format(input))

        
    else:
        flash('Error: All the form fields are required. ')
    
    return render_template('home.html', form=form)

@app.route("/predict", methods=['POST'])
def route_predict():
    return predict(request.json)


def predict(input_json):
    """Performs an sklearn prediction
        
        input looks like:
        {
        "CHAS":{
        "0":0
        },
        "RM":{
        "0":6.575
        },
        "TAX":{
        "0":296.0
        },
        "PTRATIO":{
        "0":15.3
        },
        "B":{
        "0":396.9
        },
        "LSTAT":{
        "0":4.98
        }
        
        result looks like:
        { "prediction": [ <val> ] }
        
        """
    
    # Logging the input payload
    json_payload = input_json
    LOG.info(f"JSON payload: \n{json_payload}")
    inference_payload = pd.DataFrame(json_payload)
    LOG.info(f"Inference payload DataFrame: \n{inference_payload}")
    # scale the input
    scaled_payload = scale(inference_payload)
    # get an output prediction from the pretrained model, clf
    prediction = list(clf.predict(scaled_payload))
    # TO DO:  Log the output prediction value
    LOG.info(f"prediction: {prediction}")
    return jsonify({'prediction': prediction})

if __name__ == "__main__":
    # load pretrained model as clf
    clf = joblib.load("./model_data/boston_housing_prediction.joblib")
    app.run(host='0.0.0.0', port=80, debug=True) # specify port=80
