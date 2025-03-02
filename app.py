from flask import Flask, render_template, request, redirect, url_for, session, flash
import boto3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize a session using Amazon S3
s3 = boto3.client('s3', region_name='us-east-1')

# Bucket name (replace with your actual bucket name)
BUCKET_NAME = 'your-s3-bucket-name'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Store user data in S3
        s3.put_object(Bucket=BUCKET_NAME, Key=f'users/{username}.txt', Body=hashed_password)
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            # Retrieve user data from S3
            response = s3.get_object(Bucket=BUCKET_NAME, Key=f'users/{username}.txt')
            stored_password = response['Body'].read().decode('utf-8')

            if check_password_hash(stored_password, password):
                session['username'] = username
                flash('Login successful!')
                return redirect(url_for('home'))
            else:
                flash('Invalid password.')
        except s3.exceptions.NoSuchKey:
            flash('Username not found.')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        return f'Welcome, {session["username"]}!'
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
