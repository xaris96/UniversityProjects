"""
Mars Mission Application
This application manages users for the Mars Mission project.
"""

import sqlite3
import logging
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
# Initialize Flask application
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for frontend communication

# Database file path
DB_PATH = "data/db.sqlite3"

logging.basicConfig(level=logging.DEBUG)

def init_db(testing=False):
    """Initialize the database and create the users table."""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                test_data BOOLEAN DEFAULT 0
            )
        """)

        # Insert test data if testing
        if testing:
            cursor.execute("INSERT INTO users (name, age, test_data) VALUES (?, ?, ?)",
                            ("Demo User One", 30, True))

        conn.commit()
        conn.close()
    except Exception as e:
        logging.error("Error initializing database: %s", e)
        raise

def clear_test_data():
    """Clear all test data from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE test_data = 1")
    conn.commit()
    conn.close()

# Database Functions
def get_users():
    """Retrieve all users from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def add_user(name, age, test_data=False):
    """Add a new user to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age, test_data) VALUES (?, ?, ?)",
        (name, age, test_data))
    conn.commit()
    conn.close()

def update_user(user_id, name, age):
    """Update an existing user's information."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (name, age, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    """Delete a user from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/api/users')
def api_users():
    """Return all users as JSON."""
    users = get_users()
    return jsonify([{'id': user[0], 'name': user[1], 'age': user[2]} for user in users])

@app.route('/apitest/users')
def api_test_users():
    """Return all test users as JSON."""
    users = get_users()
    test_users = [user for user in users if user[3]]  # Φιλτράρισμα μόνο για test_data=True
    return jsonify([{'id': user[0], 'name': user[1], 'age': user[2]} for user in test_users])

@app.route('/add', methods=['POST'])
def add():
    """Handle adding a new user."""
    try:
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        test_data = data.get('test_data', False)  # Default value is False
        logging.info("Data received: name=%s, age=%s, test_data=%s", name, age, test_data)
        if not name or not age:
            return jsonify({'error': 'Invalid data'}), 400
        add_user(name, age, test_data)
        return jsonify({'status': 'success'})
    except sqlite3.Error as e:
        logging.error("Database error: %s", e)
        return jsonify({'error': 'Database error'}), 500
    except ValueError as e:
        logging.error("Value error: %s", e)
        return jsonify({'error': 'Invalid value'}), 400
    except Exception as e:  # pylint: disable=broad-exception-caught
        logging.error("Unexpected error: %s", e)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/edit', methods=['POST'])
def edit():
    """Handle editing a user."""
    data = request.get_json() if request.is_json else request.form
    user_id = data.get('id')
    name = data.get('name')
    age = data.get('age')

    if not user_id or not name or not age:
        return jsonify({'error': 'Invalid data'}), 400

    update_user(user_id, name, age)
    return jsonify({'status': 'success'})

@app.route('/delete', methods=['POST'])
def delete():
    """Handle deleting a user."""
    data = request.get_json() if request.is_json else request.form
    user_id = data.get('id')

    if not user_id:
        return jsonify({'error': 'Invalid data'}), 400

    delete_user(user_id)
    return jsonify({'status': 'success'})

# Main entry point
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
