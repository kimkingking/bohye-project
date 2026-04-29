import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "diet-secret-key"

# Environment Variables for DB
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_NAME = os.environ.get('DB_NAME', 'diet_db')

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return connection

def init_db():
    """Initializes the database table if it doesn't exist."""
    # Wait a bit for DB to be ready (useful in K8s/Docker Compose)
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            cursor.execute(f"USE {DB_NAME}")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS meals (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    food_name VARCHAR(255) NOT NULL,
                    calories INT NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
            print("Database initialized successfully.")
            break
        except Error as e:
            print(f"Retrying database initialization... ({e})")
            retries -= 1
            time.sleep(5)

@app.route('/')
def index():
    conn = get_db_connection()
    meals = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM meals ORDER BY date DESC, created_at DESC")
        meals = cursor.fetchall()
        cursor.close()
        conn.close()
    else:
        flash("Could not connect to database. Please check environment variables.", "danger")
    
    return render_template('index.html', meals=meals)

@app.route('/add', methods=['POST'])
def add_meal():
    date = request.form.get('date')
    food_name = request.form.get('food_name')
    calories = request.form.get('calories')
    notes = request.form.get('notes')

    if not date or not food_name or not calories:
        flash("Please fill in all required fields.", "warning")
        return redirect(url_for('index'))

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO meals (date, food_name, calories, notes) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (date, food_name, calories, notes))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Meal added successfully!", "success")
        except Error as e:
            flash(f"Error saving to database: {e}", "danger")
    else:
        flash("Database connection failed.", "danger")

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize DB table on startup
    init_db()
    app.run(host='0.0.0.0', port=3000, debug=True)
