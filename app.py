from flask import Flask, request, jsonify, render_template
import requests
import threading
import time
import datetime
import sqlite3
from collections import Counter
import config
app = Flask(__name__)

app.config['API_KEY'] = config.API_KEY

# Configuration
API_KEY = config.API_KEY  # Replace with your OpenWeatherMap API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
UPDATE_INTERVAL = 300  # 5 minutes
TEMP_UNIT = 'Celsius'  # User preference
ALERT_THRESHOLD_TEMP = 35  # Default threshold
ALERT_CONSECUTIVE_UPDATES = 2

# Database setup
conn = sqlite3.connect('weather_data.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temperature REAL,
        humidity INTEGER,
        wind_speed REAL,
        main TEXT,
        timestamp INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        alert_message TEXT,
        timestamp INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS forecast (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temperature REAL,
        humidity INTEGER,
        wind_speed REAL,
        main TEXT,
        timestamp INTEGER
    )
''')

conn.commit()

lock = threading.Lock()

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

def fetch_weather_data():
    while True:
        for city in CITIES:
            try:
                # Fetch current weather data
                weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
                weather_response = requests.get(weather_url)
                if weather_response.status_code != 200:
                    print(f"Error fetching current data for {city}: {weather_response.text}")
                    continue
                weather_data = weather_response.json()

                # Fetch forecast data
                forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
                forecast_response = requests.get(forecast_url)
                if forecast_response.status_code != 200:
                    print(f"Error fetching forecast data for {city}: {forecast_response.text}")
                    continue
                forecast_data = forecast_response.json()

                # Process current weather data
                main_weather = weather_data['weather'][0]['main']
                temp_kelvin = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                wind_speed = weather_data['wind']['speed']
                timestamp = weather_data['dt']

                if TEMP_UNIT == 'Celsius':
                    temp = kelvin_to_celsius(temp_kelvin)
                elif TEMP_UNIT == 'Fahrenheit':
                    temp = kelvin_to_fahrenheit(temp_kelvin)
                else:
                    temp = temp_kelvin

                with lock:
                    # Insert current weather data
                    cursor.execute('''
                        INSERT INTO weather (city, temperature, humidity, wind_speed, main, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (city, temp, humidity, wind_speed, main_weather, timestamp))
                    conn.commit()

                    # Process and insert forecast data
                    for forecast in forecast_data['list']:
                        forecast_timestamp = forecast['dt']
                        forecast_temp_kelvin = forecast['main']['temp']
                        forecast_humidity = forecast['main']['humidity']
                        forecast_wind_speed = forecast['wind']['speed']
                        forecast_main_weather = forecast['weather'][0]['main']

                        if TEMP_UNIT == 'Celsius':
                            forecast_temp = kelvin_to_celsius(forecast_temp_kelvin)
                        elif TEMP_UNIT == 'Fahrenheit':
                            forecast_temp = kelvin_to_fahrenheit(forecast_temp_kelvin)
                        else:
                            forecast_temp = forecast_temp_kelvin

                        # Insert forecast data
                        cursor.execute('''
                            INSERT INTO forecast (city, temperature, humidity, wind_speed, main, timestamp)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (city, forecast_temp, forecast_humidity, forecast_wind_speed, forecast_main_weather, forecast_timestamp))
                    conn.commit()

                check_alerts(city, temp, main_weather)

            except Exception as e:
                print(f"Error fetching data for {city}: {e}")
                import traceback
                traceback.print_exc()

        time.sleep(UPDATE_INTERVAL)

def check_alerts(city, temp, main_weather):
    with lock:
        cursor.execute('''
            SELECT temperature FROM weather
            WHERE city = ? ORDER BY timestamp DESC LIMIT ?
        ''', (city, ALERT_CONSECUTIVE_UPDATES))
        temps = [record[0] for record in cursor.fetchall()]
        if len(temps) == ALERT_CONSECUTIVE_UPDATES and all(t > ALERT_THRESHOLD_TEMP for t in temps):
            alert_message = f"Temperature exceeded {ALERT_THRESHOLD_TEMP}{TEMP_UNIT[0]} for {ALERT_CONSECUTIVE_UPDATES} consecutive updates."
            cursor.execute('''
                INSERT INTO alerts (city, alert_message, timestamp)
                VALUES (?, ?, ?)
            ''', (city, alert_message, int(time.time())))
            conn.commit()
            print(f"ALERT for {city}: {alert_message}")

@app.route('/')
def index():
    return render_template('index.html', temp_unit=TEMP_UNIT, alert_threshold_temp=ALERT_THRESHOLD_TEMP)

@app.route('/update_threshold', methods=['POST'])
def update_threshold():
    global ALERT_THRESHOLD_TEMP
    ALERT_THRESHOLD_TEMP = float(request.form['threshold_temp'])
    return jsonify({'message': 'Threshold updated successfully.'})

@app.route('/get_daily_summaries', methods=['GET'])
def get_daily_summaries():
    summaries = []
    with lock:
        for city in CITIES:
            cursor.execute('''
                SELECT temperature, humidity, wind_speed, main FROM weather
                WHERE city = ? AND timestamp >= ?
            ''', (city, int(time.time()) - 86400))
            records = cursor.fetchall()
            if records:
                temps = [record[0] for record in records]
                humidities = [record[1] for record in records]
                wind_speeds = [record[2] for record in records]
                mains = [record[3] for record in records]
                avg_temp = sum(temps) / len(temps)
                max_temp = max(temps)
                min_temp = min(temps)
                avg_humidity = sum(humidities) / len(humidities)
                max_humidity = max(humidities)
                min_humidity = min(humidities)
                avg_wind_speed = sum(wind_speeds) / len(wind_speeds)
                max_wind_speed = max(wind_speeds)
                min_wind_speed = min(wind_speeds)
                dominant_weather = Counter(mains).most_common(1)[0][0]
                summaries.append({
                    'city': city,
                    'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'avg_temp': avg_temp,
                    'max_temp': max_temp,
                    'min_temp': min_temp,
                    'avg_humidity': avg_humidity,
                    'max_humidity': max_humidity,
                    'min_humidity': min_humidity,
                    'avg_wind_speed': avg_wind_speed,
                    'max_wind_speed': max_wind_speed,
                    'min_wind_speed': min_wind_speed,
                    'dominant_weather': dominant_weather
                })
    return jsonify({'summaries': summaries})

@app.route('/get_triggered_alerts', methods=['GET'])
def get_triggered_alerts():
    alerts = []
    with lock:
        cursor.execute('SELECT city, alert_message, timestamp FROM alerts ORDER BY timestamp DESC LIMIT 10')
        records = cursor.fetchall()
        for record in records:
            alerts.append({
                'city': record[0],
                'alert_message': record[1],
                'timestamp': datetime.datetime.fromtimestamp(record[2]).strftime('%Y-%m-%d %H:%M:%S')
            })
    return jsonify({'alerts': alerts})

@app.route('/get_temperature_data', methods=['GET'])
def get_temperature_data():
    datasets = []
    timestamps_set = set()
    with lock:
        for city in CITIES:
            cursor.execute('''
                SELECT timestamp, temperature FROM weather
                WHERE city = ? ORDER BY timestamp ASC
            ''', (city,))
            records = cursor.fetchall()
            if records:
                timestamps = [datetime.datetime.fromtimestamp(record[0]).strftime('%H:%M') for record in records]
                temperatures = [record[1] for record in records]
                datasets.append({
                    'label': city,
                    'data': temperatures,
                    'fill': False,
                    'borderColor': '#' + ''.join([format(ord(c), 'x') for c in city])[:6]
                })
                timestamps_set.update(timestamps)
    timestamps_sorted = sorted(list(timestamps_set))
    return jsonify({'timestamps': timestamps_sorted, 'datasets': datasets})

@app.route('/get_forecast_summaries', methods=['GET'])
def get_forecast_summaries():
    summaries = []
    with lock:
        for city in CITIES:
            cursor.execute('''
                SELECT temperature, humidity, wind_speed, main FROM forecast
                WHERE city = ? AND timestamp >= ?
            ''', (city, int(time.time())))
            records = cursor.fetchall()
            if records:
                temps = [record[0] for record in records]
                humidities = [record[1] for record in records]
                wind_speeds = [record[2] for record in records]
                mains = [record[3] for record in records]
                avg_temp = sum(temps) / len(temps)
                max_temp = max(temps)
                min_temp = min(temps)
                avg_humidity = sum(humidities) / len(humidities)
                max_humidity = max(humidities)
                min_humidity = min(humidities)
                avg_wind_speed = sum(wind_speeds) / len(wind_speeds)
                max_wind_speed = max(wind_speeds)
                min_wind_speed = min(wind_speeds)
                dominant_weather = Counter(mains).most_common(1)[0][0]
                summaries.append({
                    'city': city,
                    'avg_temp': avg_temp,
                    'max_temp': max_temp,
                    'min_temp': min_temp,
                    'avg_humidity': avg_humidity,
                    'max_humidity': max_humidity,
                    'min_humidity': min_humidity,
                    'avg_wind_speed': avg_wind_speed,
                    'max_wind_speed': max_wind_speed,
                    'min_wind_speed': min_wind_speed,
                    'dominant_weather': dominant_weather
                })
    return jsonify({'summaries': summaries})


def start_background_tasks():
    threading.Thread(target=fetch_weather_data, daemon=True).start()

if __name__ == '__main__':
    start_background_tasks()
    app.run(debug=True)
