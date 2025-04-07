from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
import os
import random
import json
from datetime import datetime, timedelta
import uuid
import sqlite3
from sqlite3 import Error
import time

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
            
            # Create bookings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id TEXT PRIMARY KEY,
                    service_type TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    postcode TEXT NOT NULL,
                    notes TEXT,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            # Create energy_usage table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS energy_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    usage REAL NOT NULL,
                    cost REAL NOT NULL
                )
            ''')
            
            # Create devices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    usage REAL,
                    generation REAL
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
            cursor.execute("SELECT COUNT(*) FROM devices")
            device_count = cursor.fetchone()[0]
            
            if device_count == 0:
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
    
    # Seed devices
    devices = [
        (1, 'Living Room Lights', 'lighting', 'on', 0.3, None),
        (2, 'Kitchen Appliances', 'appliance', 'on', 2.1, None),
        (3, 'Heating System', 'heating', 'off', 0, None),
        (4, 'EV Charger', 'charger', 'on', 5.5, None),
        (5, 'Solar Panels', 'generation', 'on', None, 3.2),
    ]
    cursor.executemany('''
        INSERT INTO devices (id, name, type, status, usage, generation)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', devices)
    
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
        print(session['user'])
        return jsonify({
            'authenticated': True,
            'user': session['user']
        })
    else:
        return jsonify({
            'authenticated': False
        })

@app.route('/api/energy/devices')
def energy_devices():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, type, status, usage, generation FROM devices")
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                device = {
                    'id': row[0],
                    'name': row[1],
                    'type': row[2],
                    'status': row[3]
                }
                
                if row[4] is not None:
                    device['usage'] = row[4]
                if row[5] is not None:
                    device['generation'] = row[5]
                
                result.append(device)
            
            return jsonify(result)
        except Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500

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

# Handle booking form submission
@app.route('/api/booking/submit', methods=['POST'])
def submit_booking():
    data = request.json
    
    # Generate a booking ID
    booking_id = str(uuid.uuid4())
    
    # Add timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bookings (
                    id, service_type, date, time, first_name, last_name, 
                    email, phone, address, city, postcode, notes, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                booking_id, 
                data.get('service_type'), 
                data.get('date'), 
                data.get('time'),
                data.get('first_name'), 
                data.get('last_name'), 
                data.get('email'), 
                data.get('phone'),
                data.get('address'), 
                data.get('city'), 
                data.get('postcode'), 
                data.get('notes', ''),
                timestamp
            ))
            conn.commit()
            
            return jsonify({
                'success': True,
                'booking_id': booking_id,
                'message': 'Booking successfully submitted'
            })
        except Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/booking/list')
def list_bookings():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, service_type, date, time, first_name, last_name, 
                email, phone, address, city, postcode, notes, timestamp
                FROM bookings ORDER BY timestamp DESC
            ''')
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                result.append({
                    'id': row[0],
                    'service_type': row[1],
                    'date': row[2],
                    'time': row[3],
                    'first_name': row[4],
                    'last_name': row[5],
                    'email': row[6],
                    'phone': row[7],
                    'address': row[8],
                    'city': row[9],
                    'postcode': row[10],
                    'notes': row[11],
                    'timestamp': row[12]
                })
            
            return jsonify(result)
        except Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500

# Update device status
@app.route('/api/energy/devices/update', methods=['POST'])
def update_device():
    data = request.json
    device_id = data.get('id')
    new_status = data.get('status')
    
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE devices SET status = ? WHERE id = ?
            ''', (new_status, device_id))
            conn.commit()
            
            # If device is turned off, set usage to 0
            if new_status == 'off':
                cursor.execute('''
                    UPDATE devices SET usage = 0 WHERE id = ? AND type != 'generation'
                ''', (device_id,))
                conn.commit()
            
            # If device is turned on, set a random usage
            if new_status == 'on':
                if device_id == 1:  # Living Room Lights
                    usage = round(random.uniform(0.1, 0.5), 2)
                elif device_id == 2:  # Kitchen Appliances
                    usage = round(random.uniform(1.2, 3.5), 2)
                elif device_id == 3:  # Heating System
                    usage = round(random.uniform(2.0, 6.0), 2)
                elif device_id == 4:  # EV Charger
                    usage = round(random.uniform(4.0, 7.0), 2)
                else:
                    usage = round(random.uniform(0.5, 2.0), 2)
                
                cursor.execute('''
                    UPDATE devices SET usage = ? WHERE id = ? AND type != 'generation'
                ''', (usage, device_id))
                conn.commit()
            
            return jsonify({
                'success': True,
                'device_id': device_id,
                'status': new_status,
                'message': f'Device {device_id} status updated to {new_status}'
            })
        except Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500

# Login route
@app.route('/api/auth/login', methods=['POST'])
def login():
    # lets get the data from the api
    data = request.json
    email = data.get('email')
    password = data.get('password')
    # Added for debugging.
    print(data)
    
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
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    })

# Serve placeholder images
@app.route('/placeholder.svg')
def placeholder():
    width = request.args.get('width', 300)
    height = request.args.get('height', 200)
    
    svg = f'''
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#f0f0f0"/>
        <text x="50%" y="50%" font-family="Arial" font-size="20" text-anchor="middle" dominant-baseline="middle" fill="#888">
            {width}x{height}
        </text>
    </svg>
    '''
    
    return svg, 200, {'Content-Type': 'image/svg+xml'}

# Add a new API endpoint to update energy usage data (for testing)
@app.route('/api/energy/usage/update', methods=['POST'])
def update_energy_usage():
    data = request.json
    date = data.get('date')
    usage = data.get('usage')
    cost = data.get('cost', round(usage * 0.28, 2))  # Default cost calculation
    
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Check if the date already exists
            cursor.execute("SELECT id FROM energy_usage WHERE date = ?", (date,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute('''
                    UPDATE energy_usage SET usage = ?, cost = ? WHERE date = ?
                ''', (usage, cost, date))
            else:
                # Insert new record
                cursor.execute('''
                    INSERT INTO energy_usage (date, usage, cost) VALUES (?, ?, ?)
                ''', (date, usage, cost))
            
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': f'Energy usage for {date} updated successfully'
            })
        except Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)