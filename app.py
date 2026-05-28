from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load trained model
rf_model = joblib.load("rf_model.pkl")

# Load vectorizer
vectorizer = joblib.load("vectorizer.pkl")

print(type(rf_model))
print(hasattr(rf_model, "estimators_"))

# Home route
@app.route('/')
def home():

    return "Phishing Detection Backend Running"

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():

    try:

        # Get JSON data
        data = request.get_json()

        # Extract email text
        email_text = data['email']

        # Transform text
        transformed_text = vectorizer.transform([email_text])

        # Predict class
        prediction = rf_model.predict(transformed_text)[0]

        # Predict probability
        probability = rf_model.predict_proba(transformed_text)[0]

        # Generate result
        if prediction == 1:
            result = "Phishing Email"
            confidence = round(probability[1] * 100, 2)

        else:
            result = "Legitimate Email"
            confidence = round(probability[0] * 100, 2)

        # Return JSON response
        return jsonify({
            "prediction": result,
            "confidence": confidence
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)