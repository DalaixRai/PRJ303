from flask import Flask, get_flashed_messages, session, render_template, request, redirect, flash,  make_response, jsonify
import pyrebase
import plotly.graph_objs as go
from datetime import datetime, timezone, timedelta,date
import base64
from io import BytesIO
import csv
import pickle
import numpy as np  # Make sure numpy is imported
from io import StringIO
import sklearn 

from io import StringIO


app = Flask(__name__)
app.secret_key = 'secret'

Config = {
    'apiKey': "AIzaSyBR2YbqKRqGCqwbjKGfsKC8lKWM4sFm3XE",
    'authDomain': "iotproject-d6843.firebaseapp.com",
    'databaseURL': "https://iotproject-d6843-default-rtdb.firebaseio.com",
    'projectId': "iotproject-d6843",
    'storageBucket': "iotproject-d6843.appspot.com",
    'messagingSenderId': "430471305958",
    'appId': "1:430471305958:web:3b315295a7eb0b4d807927",
    'measurementId': "G-JBRPJ96JN7"
  }


firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()


# Load the logistic regression model
with open('logistic_regression_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


from datetime import date, datetime, timedelta
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' in session:
        try:
            # Fetch real-time data from Firebase
            realtime_data = db.child("realtime_data").get().val()

            # Fetch threshold temperature from Firebase
            threshold_temperature = db.child("realtime_data/threshold_temperature").get().val()

            # Fetch historical data from Firebase
            historical_data = db.child("historical_data").get().val()

            # Initialize data containers
            monthly_data = {}
            weekly_data = {}
            today_data = {}

            if historical_data:
                today = date.today()
                current_year = today.year
                current_month = today.month
                start_of_week = today - timedelta(days=today.weekday())

                for date_time, data in historical_data.items():
                    datetime_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                    data_date = datetime_obj.date()
                    data_year = datetime_obj.year
                    data_month = datetime_obj.month
                    water_temperature = data.get('water_temperature')

                    if water_temperature is None:
                        continue

                    # For monthly data: check if the data point is from the current month
                    if data_year == current_year and data_month == current_month:
                        if data_date not in monthly_data or water_temperature < monthly_data[data_date]['water_temperature']:
                            monthly_data[data_date] = {
                                'datetime': datetime_obj.strftime('%Y-%m-%d %H:%M:%S'),
                                'humidity': data.get('humidity'),
                                'water_temperature': water_temperature,
                                'water_level': data.get('water_level')
                            }

                    # For weekly data: check if the data point is from the current week
                    if start_of_week <= data_date <= today:
                        if data_date not in weekly_data or water_temperature < weekly_data[data_date]['water_temperature']:
                            weekly_data[data_date] = {
                                'datetime': datetime_obj.strftime('%Y-%m-%d %H:%M:%S'),
                                'humidity': data.get('humidity'),
                                'water_temperature': water_temperature,
                                'water_level_1': data.get('water_level_1')
                            }

                    # For today data: check if the data point is from today
                    if data_date == today:
                        if data_date not in today_data or water_temperature < today_data[data_date]['water_temperature']:
                            today_data[data_date] = {
                                'datetime': datetime_obj.strftime('%Y-%m-%d %H:%M:%S'),
                                'humidity': data.get('humidity'),
                                'water_temperature': water_temperature,
                                'water_level_1': data.get('water_level_1')
                            }

            else:
                flash('No historical data found.', 'error')
        except Exception as e:
            print(f"Error fetching data: {e}")
            flash('Error fetching data.', 'error')
            monthly_data, weekly_data, today_data = {}, {}, {}

        return render_template('index.html', 
                               realtime_data=realtime_data, 
                               threshold_temperature=threshold_temperature, 
                               monthly_data=list(monthly_data.values()), 
                               weekly_data=list(weekly_data.values()), 
                               today_data=list(today_data.values()))
    
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            flash('Login successful!', 'login_success')
            return redirect('/')
        except Exception as e:
            app.logger.error('Login failed: %s', e)
            flash('Login failed. Please try again.', 'error')
            return redirect('/')

    else:
        for _ in get_flashed_messages(with_categories=False):
            pass
        return render_template('loginn.html')
    

@app.route('/set_threshold', methods=['POST'])
def set_threshold():
    if 'user' in session:
        try:
            threshold = int(request.form.get('threshold_temperature'))
            db.child("realtime_data").update({"threshold_temperature": threshold})
            flash('Threshold updated successfully!', 'success')
        except Exception as e:
            app.logger.error('Failed to update threshold: %s', e)
            flash('Failed to update threshold. Please try again.', 'error')
        return redirect('/')
    else:
        flash('You need to log in first.', 'error')
        return redirect('/')


@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    if 'user' in session:
        try:
            date_range = request.json.get('dateRange')
            start_date_str, end_date_str = date_range.split(' to ')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            # Fetch historical data from Firebase
            historical_data = db.child("historical_data").get().val()

            if not historical_data:
                flash('No data found for the selected date range.', 'error')
                return jsonify([])

            selected_data = {}

            for date_time, data in historical_data.items():
                datetime_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                data_date = datetime_obj.date()
                water_temperature = data.get('water_temperature')

                if water_temperature is None:
                    continue

                if start_date <= data_date <= end_date:
                    motors_status = data.get('motors_status')
                    motors_status = "on" if motors_status else "off"
                    
                    if data_date not in selected_data or water_temperature < selected_data[data_date]['water_temperature']:
                        selected_data[data_date] = {
                            'datetime': datetime_obj.strftime('%Y-%m-%d %H:%M:%S'),
                            'humidity': data.get('humidity'),
                            'water_temperature': water_temperature,
                            'water_current_1': data.get('water_current_1'),
                            'water_current_2': data.get('water_current_2'),
                            'water_level_1': data.get('water_level_1'),
                            'water_level_2': data.get('water_level_2'),
                            'motors_status': motors_status
                        }

            if not selected_data:
                flash('No data found for the selected date range.', 'error')

            sorted_selected_data = [selected_data[date] for date in sorted(selected_data.keys())]

            return jsonify(sorted_selected_data)

        except Exception as e:
            print(f"Error fetching data: {e}")
            flash('Error fetching data.', 'error')
            return jsonify([]), 500

    return jsonify([]), 403



@app.route('/update_plot', methods=['GET'])
def update_plot():
    if 'user' in session:
        try:
            water_temperature_data = []
            labels = []
            historical_data = {}
            data_snapshot = db.child("historical_data").get()

            if data_snapshot and data_snapshot.val():
                today = date.today()
                thirty_days_ago = today - timedelta(days=30)

                for date_time, data in data_snapshot.val().items():
                    datetime_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                    data_date = datetime_obj.date()

                    if thirty_days_ago <= data_date <= today:
                        water_temperature = data.get('water_temperature')

                        if water_temperature is not None:
                            if data_date not in historical_data or water_temperature < historical_data[data_date]['water_temperature']:
                                historical_data[data_date] = {
                                    'datetime': datetime_obj.strftime('%Y-%m-%d %H:%M:%S'),
                                    'water_temperature': water_temperature
                                }

                for day in sorted(historical_data.keys()):
                    water_temperature_data.append(historical_data[day]['water_temperature'])
                    labels.append(day.strftime('%Y-%m-%d'))
            else:
                return jsonify({'error': 'No historical data found for the last 30 days.'}), 404
        except Exception as e:
            print(f"Error fetching data: {e}")
            return jsonify({'error': str(e)}), 500

        return jsonify({'water_temperature_data': water_temperature_data, 'labels': labels})
    else:
        return jsonify({'error': 'User not authenticated'}), 401








@app.route('/predict', methods=['GET'])
def predict():
    if 'user' in session:
        try:
            realtime_data = db.child("realtime_data").get().val()
            if realtime_data:
                water_temperature = realtime_data.get('water_temperature')
                humidity = realtime_data.get('humidity')
                
                if water_temperature is not None and humidity is not None:
                    input_data = np.array([[water_temperature, humidity]])
                    prediction = model.predict(input_data)
                    motor_status = 'ON' if prediction[0] == 1 else 'OFF'
                    return jsonify({'motor_status': motor_status})
                else:
                    return jsonify({'error': 'water_temperature or humidity data missing'}), 400
            else:
                return jsonify({'error': 'No real-time data found'}), 404
        except Exception as e:
            print(f"Error making prediction: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'User not authenticated'}), 401


@app.route('/monthly')
def monthly():
    try:
        # Retrieve historical data from Firebase
        historical_data = []

        # Fetch historical data from Firebase
        data_snapshot = db.child("historical_data").get()

        if data_snapshot is not None and data_snapshot.val() is not None:
            current_month = datetime.now().month
            current_year = datetime.now().year

            daily_min_temps = {}

            # Loop through each date/time entry in historical data
            for date_time, data in data_snapshot.val().items():
                datetime_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

                # Check if the entry is in the current month and year
                if datetime_obj.month == current_month and datetime_obj.year == current_year:
                    # Extract date string (YYYY-MM-DD) for daily aggregation
                    date_str = datetime_obj.strftime('%Y-%m-%d')

                    # Extract water_temperature, humidity, and water_level from the data
                    water_temperature = data.get('water_temperature')
                    humidity = data.get('humidity')
                    water_level = data.get('water_level')

                    # Update or initialize daily minimum water_temperature
                    if date_str not in daily_min_temps or water_temperature < daily_min_temps[date_str]['water_temperature']:
                        daily_min_temps[date_str] = {
                            'datetime': datetime_obj.strftime('%Y-%m-%d %H:%M:%S'),
                            'water_temperature': water_temperature,
                            'humidity': humidity,
                            'water_level': water_level
                        }

            # Collect the daily minimum water_temperatures as a list
            historical_data = list(daily_min_temps.values())

        else:
            print("No historical data found in Firebase.")

    except Exception as e:
        print(f"Error fetching historical data: {e}")
        historical_data = []  # Initialize as empty list in case of error

    # Render the HTML template with historical_data
    return render_template('monthly.html', historical_data=historical_data)


@app.route('/download_csv', methods=['POST'])
def download_csv():
    historical_data = []
    data_snapshot = db.child("historical_data").get()

    if data_snapshot is not None and data_snapshot.val() is not None:
        for date_time, data in data_snapshot.val().items():
            datetime_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            humidity = data.get('humidity')
            water_temperature = data.get('water_temperature')
            water_current_1 = data.get('water_current_1')
            water_current_2 = data.get('water_current_2')
            water_level_1 = data.get('water_level_1')
            water_level_2 = data.get('water_level_2')
            motors_status = data.get('motors_status')

            # Convert motors_status from boolean to integer (1 or 0)
            motors_status = 1 if motors_status else 0

            data_point = {
                'datetime': datetime_obj.strftime('%Y-%m-%d %H:%M:%S'),
                'humidity': humidity,
                'water_temperature': water_temperature,
                'water_current_1': water_current_1,
                'water_current_2': water_current_2,
                'water_level_1': water_level_1,
                'water_level_2': water_level_2,
                'motors_status': motors_status
            }
            historical_data.append(data_point)

        # Generate CSV file in memory
        csv_data = StringIO()
        csv_writer = csv.DictWriter(csv_data, fieldnames=['datetime', 'humidity', 'water_temperature', 'water_current_1', 'water_current_2', 'water_level_1', 'water_level_2', 'motors_status'])
        csv_writer.writeheader()
        csv_writer.writerows(historical_data)

        # Prepare response to download the CSV file
        output = make_response(csv_data.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=historical_data.csv"
        output.headers["Content-type"] = "text/csv"
        return output
    else:
        flash('No historical data found.', 'error')
        return redirect('/')




@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        try:
            auth.send_password_reset_email(email)
            flash('Password reset instructions sent to your email.', 'success')
            return redirect('/')  # Redirect to the login page after success
        except Exception as e:
            flash('Failed to send reset instructions. Please try again.', 'error')
            return redirect('/forgot_password')

    return render_template('forgot_password.html')


def check_email_exists(email):
    try:
        # Use Firebase Authentication to check if the email exists
        user = auth.get_user_by_email(email)
        return user is not None
    except Exception as e:
        app.logger.error('Failed to check email existence: %s', e)
        return False



# @app.route('/notification')
# def notification():
#         db = firebase.database()
#         realtime_data = db.child("realtime_data").get().val()
#     # Add any necessary logic here
#         return render_template('notification.html')

@app.route('/home')
def home():
    realtime_data = None  # Initialize with a default value
    threshold_temperature = None  # Initialize with a default value
    
    if 'user' in session:
        try:
            # Fetch real-time data from Firebase
            db = firebase.database()
            realtime_data = db.child("realtime_data").get().val()
            
            # Fetch threshold temperature from Firebase
            threshold_temperature = db.child("realtime_data/threshold_temperature").get().val()
        except Exception as e:
            app.logger.error('Error fetching data: %s', e)
            flash('Error fetching data.', 'error')

    # Add any necessary logic here
    return render_template('Home.html', realtime_data=realtime_data, threshold_temperature=threshold_temperature)


@app.route('/logout', methods=['GET', 'POST'])  # Allow both GET and POST requests
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'logout_success')
    return redirect('/')

if __name__ == '__main__':
    app.run(port=1111, debug=True)
