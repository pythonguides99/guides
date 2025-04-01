from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
import os
import random
import json
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)
app.secret_key = 'rolsa_technologies_secret_key'

# Create a directory for static files if it doesn't exist
os.makedirs('static', exist_ok=True)

# Move HTML files to templates directory
os.makedirs('templates', exist_ok=True)

# Store bookings in memory (in a real app, this would be a database)
bookings = []

# Generate false energy data
def generate_energy_data():
    # Generate random daily usage for the past 30 days
    daily_usage = []
    today = datetime.now()
    
    for i in range(30):
        date = today - timedelta(days=i)
        # Generate random usage between 8 and 25 kWh
        usage = round(random.uniform(8, 25), 1)
        daily_usage.append({
            'date': date.strftime('%Y-%m-%d'),
            'usage': usage,
            'cost': round(usage * 0.28, 2)  # Assuming £0.28 per kWh
        })
    
    # Sort by date (oldest first)
    daily_usage.sort(key=lambda x: x['date'])
    
    return daily_usage

# Generate false device data
def generate_device_data():
    devices = [
        {'id': 1, 'name': 'Living Room Lights', 'type': 'lighting', 'status': 'on', 'usage': round(random.uniform(0.1, 0.5), 2)},
        {'id': 2, 'name': 'Kitchen Appliances', 'type': 'appliance', 'status': 'on', 'usage': round(random.uniform(1.2, 3.5), 2)},
        {'id': 3, 'name': 'Heating System', 'type': 'heating', 'status': 'off', 'usage': 0},
        {'id': 4, 'name': 'EV Charger', 'type': 'charger', 'status': 'on', 'usage': round(random.uniform(4.0, 7.0), 2)},
        {'id': 5, 'name': 'Solar Panels', 'type': 'generation', 'status': 'on', 'generation': round(random.uniform(2.0, 5.0), 2)},
    ]
    return devices

# Generate false recommendations
def generate_recommendations():
    recommendations = [
        {'id': 1, 'title': 'Reduce Heating Usage', 'description': 'Lower your thermostat by 1°C to save up to 10% on heating costs.', 'savings': '£120/year'},
        {'id': 2, 'title': 'Upgrade to LED Lighting', 'description': 'Replace remaining halogen bulbs with LEDs to reduce lighting energy use by 80%.', 'savings': '£45/year'},
        {'id': 3, 'title': 'Install Smart Power Strips', 'description': 'Eliminate phantom energy usage from devices on standby.', 'savings': '£65/year'},
        {'id': 4, 'title': 'Optimize EV Charging Times', 'description': 'Charge your EV during off-peak hours to benefit from lower rates.', 'savings': '£180/year'},
        {'id': 5, 'title': 'Add Battery Storage', 'description': 'Store excess solar energy for use during peak hours.', 'savings': '£350/year'},
    ]
    return recommendations

# Routes
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/index.html')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/booking.html')
def booking():
    return send_from_directory('.', 'booking.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

# API endpoints for false data
@app.route('/api/energy/usage')
def energy_usage():
    return jsonify(generate_energy_data())

@app.route('/api/energy/devices')
def energy_devices():
    return jsonify(generate_device_data())

@app.route('/api/energy/recommendations')
def energy_recommendations():
    return jsonify(generate_recommendations())

@app.route('/api/energy/summary')
def energy_summary():
    # Generate a summary of energy usage
    daily_usage = generate_energy_data()
    
    # Calculate total usage and cost
    total_usage = sum(day['usage'] for day in daily_usage)
    total_cost = sum(day['cost'] for day in daily_usage)
    
    # Calculate averages
    avg_daily_usage = total_usage / len(daily_usage)
    avg_daily_cost = total_cost / len(daily_usage)
    
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
    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['booking_id'] = booking_id
    
    # Store the booking
    bookings.append(data)
    
    return jsonify({
        'success': True,
        'booking_id': booking_id,
        'message': 'Booking successfully submitted'
    })

@app.route('/api/booking/list')
def list_bookings():
    return jsonify(bookings)

# Update device status
@app.route('/api/energy/devices/update', methods=['POST'])
def update_device():
    data = request.json
    device_id = data.get('id')
    new_status = data.get('status')
    
    # In a real app, this would update a database
    # For now, we just return success
    return jsonify({
        'success': True,
        'device_id': device_id,
        'status': new_status,
        'message': f'Device {device_id} status updated to {new_status}'
    })

# Login simulation
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Very simple authentication (in a real app, this would check a database)
    if email == 'user@example.com' and password == 'password':
        session['logged_in'] = True
        session['user'] = {
            'name': 'Max Johnson',
            'email': email,
            'role': 'user'
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
