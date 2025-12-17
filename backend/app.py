from flask import Flask, jsonify
from flask_cors import CORS  # <-- import CORS

app = Flask(__name__)
CORS(app)  # <-- allow cross-origin requests

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

if __name__ == "__main__":
    app.run(debug=True)
