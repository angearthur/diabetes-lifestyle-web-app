from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

# ✅ NEW: submit patient data
@app.route('/submit-data', methods=['POST'])
def submit_data():
    data = request.json
    return jsonify({
        "status": "success",
        "received": data
    })

# ⚠️ This must stay at the very bottom
if __name__ == "__main__":
    app.run(debug=True)
