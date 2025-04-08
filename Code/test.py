from flask import Flask, request, send_from_directory, jsonify, session
import sqlite3
from sqlite3 import Error
import os
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'rolsa_technologies_secret_key'

# Database setup
DATABASE_FILE = "rolsa_energy.db"

def create_connection():
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except Error as e:
        print(e)
    return conn

def create_tables():
    """Create the necessary tables if they don't exist"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Create energy_usage table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS energy_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    usage REAL NOT NULL,
                    cost REAL NOT NULL
                )
            ''')
            
            # Create recommendations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    savings TEXT NOT NULL
                )
            ''')
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            
            # Check if we need to seed the database
            cursor.execute("SELECT COUNT(*) FROM recommendations")
            rec_count = cursor.fetchone()[0]
            
            if rec_count == 0:
                seed_database(conn)
                
        except Error as e:
            print(e)
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")

def seed_database(conn):
    """Seed the database with initial data"""
    cursor = conn.cursor()
    
    # Seed recommendations
    recommendations = [
        (1, 'Reduce Heating Usage', 'Lower your thermostat by 1°C to save up to 10% on heating costs.', '£120/year'),
        (2, 'Upgrade to LED Lighting', 'Replace remaining halogen bulbs with LEDs to reduce lighting energy use by 80%.', '£45/year'),
        (3, 'Install Smart Power Strips', 'Eliminate phantom energy usage from devices on standby.', '£65/year'),
        (4, 'Optimize EV Charging Times', 'Charge your EV during off-peak hours to benefit from lower rates.', '£180/year'),
        (5, 'Add Battery Storage', 'Store excess solar energy for use during peak hours.', '£350/year'),
    ]
    cursor.executemany('''
        INSERT INTO recommendations (id, title, description, savings)
        VALUES (?, ?, ?, ?)
    ''', recommendations)
    
    # Seed energy usage data for the past 30 days
    today = datetime.now()
    energy_usage = []
    
    for i in range(30):
        date = today - timedelta(days=i)
        # Generate random usage between 8 and 25 kWh
        usage = round(random.uniform(8, 25), 1)
        cost = round(usage * 0.28, 2)  # Assuming £0.28 per kWh
        energy_usage.append((date.strftime('%Y-%m-%d'), usage, cost))
    
    cursor.executemany('''
        INSERT INTO energy_usage (date, usage, cost)
        VALUES (?, ?, ?)
    ''', energy_usage)
    
    # Seed a test user
    cursor.execute('''
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, ?)
    ''', ('Max Johnson', 'user@example.com', 'password', 'user'))
    
    conn.commit()

# Initialize database
create_tables()

# Routes
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/index')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/booking')
def booking():
    return send_from_directory('.', 'booking.html')

@app.route('/login')
def viewlogin():
    return send_from_directory('.', 'login.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

# API endpoints for data
@app.route('/api/energy/usage')
def energy_usage():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT date, usage, cost FROM energy_usage ORDER BY date")
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                result.append({
                    'date': row[0],
                    'usage': row[1],
                    'cost': row[2]
                })
            
            return jsonify(result)
        except Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500
    
@app.route('/api/auth/check')
def check_auth():
    if 'logged_in' in session and session['logged_in'] and 'user' in session:
        return jsonify({
            'authenticated': True,
            'user': session['user']
        })
    else:
        return jsonify({
            'authenticated': False
        })

@app.route('/api/energy/recommendations')
def energy_recommendations():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, description, savings FROM recommendations")
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                result.append({
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'savings': row[3]
                })
            
            return jsonify(result)
        except Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/energy/summary')
def energy_summary():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(usage), SUM(cost), COUNT(*) FROM energy_usage")
            row = cursor.fetchone()
            
            total_usage = row[0]
            total_cost = row[1]
            days = row[2]
            
            avg_daily_usage = total_usage / days if days > 0 else 0
            avg_daily_cost = total_cost / days if days > 0 else 0
            
            # Calculate savings (fictional)
            savings_percentage = random.uniform(12, 25)
            cost_savings = (total_cost * savings_percentage) / 100
            
            # Generate random carbon footprint reduction
            carbon_reduction = round(total_usage * 0.4 * random.uniform(0.8, 1.2), 1)  # 0.4 kg CO2 per kWh
            
            return jsonify({
                'total_usage': round(total_usage, 1),
                'total_cost': round(total_cost, 2),
                'avg_daily_usage': round(avg_daily_usage, 1),
                'avg_daily_cost': round(avg_daily_cost, 2),
                'savings_percentage': round(savings_percentage, 1),
                'cost_savings': round(cost_savings, 2),
                'carbon_reduction': carbon_reduction
            })
        except Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/energy/real-time')
def energy_real_time():
    # Generate real-time energy data
    current_usage = round(random.uniform(0.8, 3.5), 2)
    solar_generation = round(random.uniform(0, 2.5), 2) if 6 <= datetime.now().hour <= 20 else 0
    grid_usage = max(0, current_usage - solar_generation)
    
    return jsonify({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'current_usage': current_usage,
        'solar_generation': solar_generation,
        'grid_usage': grid_usage,
        'unit': 'kW'
    })

# Login route
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, email, role FROM users 
                WHERE email = ? AND password = ?
            ''', (email, password))
            user = cursor.fetchone()
            
            if user:
                session['logged_in'] = True
                session['user'] = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'role': user[3]
                }
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'user': session['user']
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid email or password'
                }), 401
        except Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    # Clear the session so that that user is logged out
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')  # Default role is 'user'

    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Check if the email already exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                return jsonify({
                    'success': False,
                    'message': 'Email already registered'
                }), 400
            
            # Insert the new user
            cursor.execute('''
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, ?)
            ''', (name, email, password, role))
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Registration successful'
            })
        except Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
