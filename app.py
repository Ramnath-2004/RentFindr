from flask import Flask, redirect, render_template, session , request, jsonify, send_file, send_from_directory, url_for
from flask_cors import CORS
from flask_mail import Mail, Message
from pymongo import MongoClient
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set your secret key for session management
CORS(app)  # Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})


# Flask-Mail configuration for email sending
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
app.config['MAIL_DEBUG'] = True

mail = Mail(app)

# MongoDB configuration
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['Gokuldb']  # Database name

# Load the dataset and preprocess it
data = pd.read_csv("Districts.csv")
data['Sqft'] = data['Sqft'].str.replace(',', '').astype(float)  # Convert Sqft to float
data_encoded = pd.get_dummies(data, columns=['District'])

# Split the dataset into features (X) and target variable (y)
X = data_encoded.drop(columns=["Price", "Address", "Predicted Price"])
y = data_encoded["Price"]

# Train the Random Forest model
rf_model = RandomForestRegressor(n_estimators=700, max_depth=10, min_samples_split=5, min_samples_leaf=2, random_state=42)  
rf_model.fit(X, y)

@app.route('/')
def index():
    user_logged_in = 'username' in session  # Check if the user is logged in
    username = session.get('username')  # Get the username from the session
    looking_for = session.get('looking_for')  # Get the 'Looking For' data from the session
    return render_template('index.html', user_logged_in=user_logged_in, username=username, looking_for=looking_for)

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    return redirect('/')


@app.route('/about.html')
def about():
    user_logged_in = 'username' in session  # Check if the user is logged in
    username = session.get('username')  # Get the username from the session
    looking_for = session.get('looking_for')  # Get the 'Looking For' data from the session
    return render_template('about.html', user_logged_in=user_logged_in, username=username, looking_for=looking_for)

@app.route('/property-grid.html')
def property():
    user_logged_in = 'username' in session  # Check if the user is logged in
    username = session.get('username')  # Get the username from the session
    looking_for = session.get('looking_for')  # Get the 'Looking For' data from the session
    return render_template('property-grid.html', user_logged_in=user_logged_in, username=username, looking_for=looking_for)

@app.route('/contact.html')
def contact():
    user_logged_in = 'username' in session  # Check if the user is logged in
    username = session.get('username')  # Get the username from the session
    looking_for = session.get('looking_for')  # Get the 'Looking For' data from the session
    return render_template('contact.html', user_logged_in=user_logged_in, username=username, looking_for=looking_for)


@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/property-single1.html')
def property_single1():
    user_logged_in = 'username' in session  # Check if the user is logged in
    username = session.get('username')  # Get the username from the session
    looking_for = session.get('looking_for')  # Get the 'Looking For' data from the session
    return render_template('property-single1.html', user_logged_in=user_logged_in, username=username, looking_for=looking_for)

@app.route('/property-single2.html')
def property_single2():
    user_logged_in = 'username' in session  # Check if the user is logged in
    username = session.get('username')  # Get the username from the session
    looking_for = session.get('looking_for')  # Get the 'Looking For' data from the session
    return render_template('property-single2.html', user_logged_in=user_logged_in, username=username, looking_for=looking_for)

@app.route('/property-single3.html')
def property_single3():
    user_logged_in = 'username' in session  # Check if the user is logged in
    username = session.get('username')  # Get the username from the session
    looking_for = session.get('looking_for')  # Get the 'Looking For' data from the session
    return render_template('property-single3.html', user_logged_in=user_logged_in, username=username, looking_for=looking_for)

@app.route('/property-single4.html')
def property_single4():
    user_logged_in = 'username' in session  # Check if the user is logged in
    username = session.get('username')  # Get the username from the session
    looking_for = session.get('looking_for')  # Get the 'Looking For' data from the session
    return render_template('property-single4.html', user_logged_in=user_logged_in, username=username, looking_for=looking_for)

@app.route('/property-single5.html')
def property_single5():
    user_logged_in = 'username' in session  # Check if the user is logged in
    username = session.get('username')  # Get the username from the session
    looking_for = session.get('looking_for')  # Get the 'Looking For' data from the session
    return render_template('property-single5.html', user_logged_in=user_logged_in, username=username, looking_for=looking_for)

@app.route('/property-single6.html')
def property_single6():
    user_logged_in = 'username' in session  # Check if the user is logged in
    username = session.get('username')  # Get the username from the session
    looking_for = session.get('looking_for')  # Get the 'Looking For' data from the session
    return render_template('property-single6.html', user_logged_in=user_logged_in, username=username, looking_for=looking_for)

@app.route('/property-single7.html')
def property_single7():
    user_logged_in = 'username' in session  # Check if the user is logged in
    username = session.get('username')  # Get the username from the session
    looking_for = session.get('looking_for')  # Get the 'Looking For' data from the session
    return render_template('property-single7.html', user_logged_in=user_logged_in, username=username, looking_for=looking_for)

@app.route('/test_css')
def test_css():
    return f'<link rel="stylesheet" href="{url_for("static", filename="assets/css/style.css")}">'

@app.route('/templates/nav.html')
def nav():
    return render_template('nav.html')

@app.route('/templates/footer.html')
def footer():
    return render_template('footer.html')


@app.route('/predict', methods=['POST'])
def predict():
    sqft = float(request.form['sqft'])
    district = request.form['district']

    # Prepare input data for prediction
    input_data = pd.DataFrame({
        'Sqft': [sqft],
        **{f'District_{district}': [1]}
    })
    for col in X.columns:
        if col not in input_data.columns:
            input_data[col] = 0
    input_data = input_data[X.columns]

    # Make prediction
    predicted_price = rf_model.predict(input_data)[0]

    # Return as plain text for the modal
    return f'Predicted Price: ₹{predicted_price:.2f}'

# Email sending endpoint
@app.route('/send', methods=['POST'])
def send_email():
    try:
        data = request.json
        print('Received data:', data)
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        # Compose the email
        msg = Message(
            subject=f"New Contact Form Submission: {subject}",
            sender=app.config['MAIL_USERNAME'],
            recipients=['rentfindr@gmail.com']  # Your receiving email
        )
        msg.html = f"""
            <h3>New Contact Form Message</h3>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
        """
        mail.send(msg)

        return jsonify({'message': 'Email sent successfully'})
    except Exception as e:
        print('Error sending email:', e)
        return jsonify({'message': 'Error sending email'}), 500
    

    # Signup route
@app.route('/signup', methods=['POST'])
def signup_user():
    data = request.get_json()  # If using JSON for form submission

    # Get the form data
    full_name = data.get("fullName")
    email = data.get("email")
    
    password = data.get("password")
    confirm_password = data.get("confirmPassword")
    looking_for = data.get("lookingFor")  # Collect looking for option

    # Check if passwords match
    if password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    try:
        # Insert new user data into the 'users' collection
        users_collection = db["users"]
        new_user = {
            "fullName": full_name,
            "email": email,
            "password": password,
            "lookingFor": looking_for  # Store 'Looking For' in camelCase
        }
        users_collection.insert_one(new_user)

        # Optionally, you can save the user's info in the session
        session['username'] = full_name
        session['looking_for'] = looking_for  # Store 'Looking For' in session

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as error:
        logging.error("Error registering user: %s", error)
        return jsonify({"message": "Error registering user"}), 500


# Login route
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        users_collection = db["users"]
        user = users_collection.find_one({"email": email})

        if not user:
            return jsonify({"message": "User not found"}), 404

        if user["password"] != password:
            return jsonify({"message": "Incorrect password"}), 401

        # Set session after successful login
        session['username'] = user.get('fullName')  # or user.get('email'), depending on your preference

        # Send a success response
        return jsonify({"message": "Login successful"}), 200
    except Exception as error:
        logging.error("Error logging in: %s", error)
        return jsonify({"message": "Error logging in"}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
