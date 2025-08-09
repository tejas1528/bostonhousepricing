import json
import pickle
from flask import Flask, request, app, jsonify, render_template, url_for
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the pre-trained model
regmodel = pickle.load(open('regmodel.pkl', 'rb'))
scalar = pickle.load(open('scaler.pkl', 'rb'))  

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.get_json()
    data = data['data']
    print(data)
    print(np.array(list(data.values())).reshape(1, -1))
    new_data = scalar.transform(np.array(list(data.values())).reshape(1, -1))
    output = regmodel.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict', methods=['POST'])
def predict():
    # Feature names in correct order
    features = ["CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"]

    try:
        data = [float(request.form.get(f)) for f in features]
    except (TypeError, ValueError):
        return render_template('home.html', prediction_text='Invalid input — please enter valid numbers.')

    final_input = scalar.transform(np.array(data).reshape(1, -1))
    output = regmodel.predict(final_input)
    return render_template('home.html', prediction_text=f'The predicted house price is {output[0]}')

if __name__ == '__main__':
    app.run(debug=True)
    