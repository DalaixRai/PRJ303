import pyrebase

# Config = {
#     'apiKey': "AIzaSyC4TNQl40Lccy-nr0uPnVYXVYVqZ89dE6Y",
#     'authDomain': "dht11-firebase-3094c.firebaseapp.com",
#     'databaseURL': "https://dht11-firebase-3094c-default-rtdb.asia-southeast1.firebasedatabase.app",
#     'projectId': "dht11-firebase-3094c",
#     'storageBucket': "dht11-firebase-3094c.appspot.com",
#     'messagingSenderId': "421392299639",
#     'appId': "1:421392299639:web:cb664a71ab1aed5dc4b872",
#     'measurementId': "G-YQBKBDKJ42",
#   }

# Config = {
#   'apiKey': "AIzaSyCXwReP9X4XHIfevrMsg6c6E1WKGU-oHVE",
#   'authDomain': "esp32-with-dht22-4829e.firebaseapp.com",
#   'databaseURL': "https://esp32-with-dht22-4829e-default-rtdb.firebaseio.com",
#   'projectId': "esp32-with-dht22-4829e",
#   'storageBucket': "esp32-with-dht22-4829e.appspot.com",
#   'messagingSenderId': "431637432916",
#   'appId': "1:431637432916:web:0c04e49f68ed5c19a6bbc1",
#   'measurementId': "G-XR07N2ZY7B"
# }

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

email = 'test@gmail.com'
name = "Dawa"
Role = "Plumber"
password = '12345678'


user = auth.create_user_with_email_and_password(email,password)
print(user)

user = auth.sign_in_with_email_and_password(email, password)

info = auth.get_account_info(user['idToken'])
print(info)

auth.send_email_verification(user['idToken'])
auth.send_password_reset_email(email)