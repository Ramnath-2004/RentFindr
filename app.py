from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
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
CORS(app)  # Enable CORS for all routes
# CORS(app, resources={r"/*": {"origins": "*"}})


# Flask-Mail configuration for email sending
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
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
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/property-grid.html')
def property():
    return render_template('property-grid.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/property-single1.html')
def property_single1():
    return render_template('property-single1.html')

@app.route('/property-single2.html')
def property_single2():
    return render_template('property-single2.html')

@app.route('/property-single3.html')
def property_single3():
    return render_template('property-single3.html')

@app.route('/property-single4.html')
def property_single4():
    return render_template('property-single4.html')

@app.route('/property-single5.html')
def property_single5():
    return render_template('property-single5.html')

@app.route('/property-single6.html')
def property_single6():
    return render_template('property-single6.html')

@app.route('/property-single7.html')
def property_single7():
    return render_template('property-single7.html')

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

if __name__ == '__main__':
    app.run(debug=True)
