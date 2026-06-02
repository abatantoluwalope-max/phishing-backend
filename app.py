from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re

# Initialize Flask app

app = Flask(**name**)
CORS(app)

# Load trained model

rf_model = joblib.load("rf_model.pkl")

# Load vectorizer

vectorizer = joblib.load("vectorizer.pkl")

print("Model Loaded Successfully")

@app.route('/')
def home():
return "AI Phishing Threat Intelligence Backend Running"

def detect_patterns(email_text):

```
patterns = []

text = email_text.lower()

urgency_words = [
    "urgent",
    "immediately",
    "verify now",
    "act now",
    "suspended",
    "limited time",
    "expired",
    "warning"
]

credential_words = [
    "password",
    "login",
    "signin",
    "verify account",
    "confirm account",
    "update account"
]

financial_words = [
    "bank",
    "payment",
    "credit card",
    "transaction",
    "invoice",
    "wire transfer"
]

if any(word in text for word in urgency_words):
    patterns.append("Urgency Language")

if any(word in text for word in credential_words):
    patterns.append("Credential Request")

if any(word in text for word in financial_words):
    patterns.append("Financial Scam Indicators")

if re.search(r"http[s]?://", text):
    patterns.append("Suspicious URL")

if "click here" in text:
    patterns.append("Call-To-Action Link")

if len(patterns) == 0:
    patterns.append("No Major Indicators Detected")

return patterns
```

def get_risk_level(confidence, prediction):

```
if prediction == "Legitimate Email":
    return "Safe"

if confidence >= 95:
    return "Critical"

elif confidence >= 85:
    return "High"

elif confidence >= 70:
    return "Medium"

return "Low"
```

def generate_explanation(prediction, patterns):

```
if prediction == "Legitimate Email":

    return (
        "The email does not contain strong phishing indicators "
        "and appears to be legitimate based on the machine learning analysis."
    )

return (
    "The email contains phishing-related characteristics such as "
    + ", ".join(patterns)
    + ". These indicators are commonly associated with phishing attacks."
)
```

@app.route('/predict', methods=['POST'])
def predict():

```
try:

    data = request.get_json()

    email_text = data['email']

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

    explanation = generate_explanation(result, patterns)

    return jsonify({
        "prediction": result,
        "confidence": confidence,
        "risk_level": risk_level,
        "detected_patterns": patterns,
        "explanation": explanation
    })

except Exception as e:

    return jsonify({
        "error": str(e)
    })
```

if **name** == "**main**":
app.run(host="0.0.0.0", port=10000)
