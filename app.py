from flask import Flask, render_template, request, redirect, url_for, session, flash
import boto3
import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection
db_config = {
    'user': 'admin',  # Your RDS username
    'password': 'your_rds_password',  # Your RDS password
    'host': 'your_rds_endpoint',  # Your RDS endpoint
    'database': 'your_database_name'  # Your database name
}

# Initialize S3 client
s3 = boto3.client('s3', region_name='us-east-1')
BUCKET_NAME = 'flask-image-uploads'  # Your S3 bucket name

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
        file = request.files['file']
        if file:
            s3.upload_fileobj(file, BUCKET_NAME, file.filename)
            flash('Image uploaded successfully!')
            return redirect(url_for('upload'))
    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
