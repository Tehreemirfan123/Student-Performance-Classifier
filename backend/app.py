from flask import Flask, request, jsonify # type: ignore
import joblib # type: ignore
import numpy as np # type: ignore
import pandas as pd # type: ignore
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}}) 

# Load the saved model and encoders
model = joblib.load('../model/student_classifier.pkl')
label_encoders = {}
try:
    label_encoders = joblib.load('../model/label_encoders.joblib')
except FileNotFoundError:
    print("No label encoders found, proceeding without them.")

# Features expected by the model
FEATURES = ['studytime', 'absences', 'failures', 'Medu', 'Fedu', 'G1', 'G2']

# Grade labels
GRADE_LABELS = ['F', 'D', 'C', 'B', 'A']

def preprocess_input(data):
    """
    Preprocess input data dict to model input vector
    """
    # Extract features with defaults if missing
    inputs = []
    for feature in FEATURES:
        val = data.get(feature)
        if val is None:
            return None, f"Missing feature: {feature}"
        inputs.append(val)

    # Convert to numpy array (1, n_features)
    X = np.array(inputs).reshape(1, -1)

    # If you had label encoding on features, apply here (your current features are numeric, so skip)

    return X, None

@app.route('/predict', methods=['POST'])
def predict():
    """
    Expects JSON input with features:
    {
        "studytime": int,
        "absences": int,
        "failures": int,
        "Medu": int,
        "Fedu": int,
        "G1": int,
        "G2": int
    }
    Returns predicted grade and probabilities
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    X, error = preprocess_input(data)
    if error:
        return jsonify({'error': error}), 400

    # Predict grade label
    pred_label = model.predict(X)[0]
    pred_proba = model.predict_proba(X)[0]

    # Build response with predicted grade and confidence scores
    proba_dict = {grade: float(prob) for grade, prob in zip(model.classes_, pred_proba)}

    response = {
        'predicted_grade': pred_label,
        'probabilities': proba_dict
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')