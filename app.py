from flask import Flask, render_template, request, redirect, url_for, session, flash
import boto3
import mysql.connector
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Add logging configuration
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection
db_config = {
    'user': 'widhi',  # Your RDS username
    'password': 'b1sm1llah',  # Your RDS password
    'host': 'appdb.ctycq9qeemfp.us-east-1.rds.amazonaws.com',  # Your RDS endpoint
    'database': 'app_db'  # Your database name
}

# Initialize S3 client
s3 = boto3.client('s3', region_name='us-east-1')
#aws_access_key_id='ASIA6AOHVJRAEQOKSGH3',
#aws_secret_access_key='zd3KzpO3kYaZErA1g81CE42YJBwrwJTSRKwk8s/M')
BUCKET_NAME = 'web-app212'  # Your S3 bucket name
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')  # Ensure you have an index.html file


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Store user data in RDS
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve user data from RDS
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result and check_password_hash(result[0], password):
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('upload'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part in the request')
            return redirect(request.url)
            
        file = request.files['file']
        
        # If user does not select file, browser also submits empty part
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            try:
                # Create secure filename with UUID to avoid overwriting
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                
                # Upload to S3
                s3.upload_fileobj(file, BUCKET_NAME, unique_filename)
                flash('Image uploaded successfully!')
                
                # Optionally log the successful upload
                logging.info(f"User {session['username']} uploaded file {unique_filename} to bucket {BUCKET_NAME}")
                
                return redirect(url_for('upload'))
            except Exception as e:
                # Log the error and show user-friendly message
                logging.error(f"S3 upload error: {str(e)}")
                flash('Failed to upload image. Please try again later.')
                return redirect(url_for('upload'))
        else:
            flash('Invalid file type. Allowed types: png, jpg, jpeg, gif')
            return redirect(url_for('upload'))
            
    return render_template('upload.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
