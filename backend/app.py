from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Test route
@app.route('/')
def home():
    return jsonify({"message": "Hello! Backend is working."})

# Patient route
@app.route('/patient', methods=['GET'])
def patient_info():
    sample_data = {
        "name": "John Doe",
        "age": 45,
        "weight": 80,
        "blood_sugar": 120
    }
    return jsonify(sample_data)

# Submit patient data with health analysis
@app.route('/submit-data', methods=['POST'])
def submit_data():
    data = request.json

    # Convert inputs to numbers safely
    blood_sugar = float(data.get("blood_sugar", 0))
    weight = float(data.get("weight", 0))

    advice = []

    # Blood sugar analysis
    if blood_sugar > 140:
        advice.append("High blood sugar detected. Reduce sugar intake and exercise regularly.")
    else:
        advice.append("Blood sugar level is within a healthy range.")

    # Weight analysis
    if weight > 90:
        advice.append("Weight is above recommended range. Consider a balanced diet and physical activity.")
    else:
        advice.append("Weight is within a healthy range.")

    return jsonify({
        "status": "success",
        "patient": data,
        "recommendations": advice
    })

# This must stay at the very bottom
if __name__ == "__main__":
    app.run(debug=True)
