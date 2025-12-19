import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_NAME = "patients.db"

# -------------------------------------------------
# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            weight REAL,
            height REAL,
            blood_sugar REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------------------------------------
# Home route
@app.route("/")
def home():
    return jsonify({"message": "Diabetes Lifestyle Backend Running"})

# -------------------------------------------------
# Submit patient data
@app.route("/submit-data", methods=["POST"])
def submit_data():
    data = request.json

    name = data.get("name")
    age = int(data.get("age", 0))
    weight = float(data.get("weight", 0))       # kg
    height = float(data.get("height", 1.7))     # meters (default safety)
    blood_sugar = float(data.get("blood_sugar", 0))  # mg/dL (fasting)

    # -------------------------------------------------
    # Save to database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (name, age, weight, height, blood_sugar)
        VALUES (?, ?, ?, ?, ?)
    """, (name, age, weight, height, blood_sugar))
    conn.commit()
    conn.close()

    # -------------------------------------------------
    # BLOOD SUGAR ANALYSIS (Fasting)
    if blood_sugar < 70:
        sugar_status = "🔴 Hypoglycemia (Too Low)"
        sugar_advice = "Immediate medical attention recommended."
    elif 70 <= blood_sugar <= 99:
        sugar_status = "🟢 Normal Blood Sugar"
        sugar_advice = "Maintain healthy diet and regular exercise."
    elif 100 <= blood_sugar <= 125:
        sugar_status = "🟡 Prediabetes"
        sugar_advice = "Lifestyle changes needed to prevent diabetes."
    else:
        sugar_status = "🔴 Diabetes (High Risk)"
        sugar_advice = "Consult a healthcare provider for treatment."

    # -------------------------------------------------
    # BMI CALCULATION
    bmi = round(weight / (height ** 2), 1)

    if bmi < 18.5:
        bmi_status = "🔴 Underweight"
    elif 18.5 <= bmi <= 24.9:
        bmi_status = "🟢 Normal weight"
    elif 25 <= bmi <= 29.9:
        bmi_status = "🟡 Overweight"
    elif 30 <= bmi <= 34.9:
        bmi_status = "🔴 Obesity Class I"
    elif 35 <= bmi <= 39.9:
        bmi_status = "🔴 Obesity Class II"
    else:
        bmi_status = "🔴 Obesity Class III"

    # -------------------------------------------------
    # AGE RISK ANALYSIS
    if age < 45:
        age_risk = "🟢 Low diabetes risk by age"
    elif 45 <= age <= 64:
        age_risk = "🟡 Medium diabetes risk – screening recommended"
    else:
        age_risk = "🔴 High diabetes risk – regular monitoring required"

    # -------------------------------------------------
    # RESPONSE
    return jsonify({
        "status": "success",
        "patient": {
            "name": name,
            "age": age,
            "weight": weight,
            "height": height,
            "blood_sugar": blood_sugar
        },
        "clinical_analysis": {
            "blood_sugar_status": sugar_status,
            "blood_sugar_advice": sugar_advice,
            "bmi": bmi,
            "bmi_status": bmi_status,
            "age_risk": age_risk
        }
    })

# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)



