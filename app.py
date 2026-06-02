from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re

app = Flask(__name__)
CORS(app)

rf_model = joblib.load("rf_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


@app.route("/")
def home():
    return "AI Phishing Threat Intelligence Backend Running"


def detect_patterns(email_text):

    patterns = []

    text = email_text.lower()

    if "urgent" in text:
        patterns.append("Urgency Language")

    if "password" in text or "login" in text:
        patterns.append("Credential Request")

    if "http://" in text or "https://" in text:
        patterns.append("Suspicious URL")

    if "click here" in text:
        patterns.append("Call-To-Action Link")

    if len(patterns) == 0:
        patterns.append("No Major Indicators Detected")

    return patterns


def get_risk_level(confidence, prediction):

    if prediction == "Legitimate Email":
        return "Safe"

    if confidence >= 95:
        return "Critical"

    if confidence >= 85:
        return "High"

    if confidence >= 70:
        return "Medium"

    return "Low"


@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        email_text = data["email"]

        transformed_text = vectorizer.transform([email_text])

        prediction = rf_model.predict(transformed_text)[0]

        probability = rf_model.predict_proba(transformed_text)[0]

        if prediction == 1:
            result = "Phishing Email"
            confidence = round(probability[1] * 100, 2)
        else:
            result = "Legitimate Email"
            confidence = round(probability[0] * 100, 2)

        patterns = detect_patterns(email_text)

        risk_level = get_risk_level(confidence, result)

        return jsonify({
            "prediction": result,
            "confidence": confidence,
            "risk_level": risk_level,
            "detected_patterns": patterns
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)