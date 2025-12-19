import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect('patients.db')
cursor = conn.cursor()

# Create patients table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    weight REAL,
    blood_sugar REAL
)
''')

conn.commit()
conn.close()

print("Database and 'patients' table are ready!")
