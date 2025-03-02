# AWS Module: EC2, S3, RDS for a simple webapp

## Overview
This project is a simple web application built using Flask that simulates a DevOps workflow in AWS. The application allows users to register, log in, and upload images. User credentials are stored in an Amazon RDS database, while images are uploaded to an Amazon S3 bucket.

## Features
- User registration and login functionality
- Image upload to Amazon S3
- User data stored in Amazon RDS

## Prerequisites
- An AWS account
- Basic knowledge of Python and Flask
- AWS CLI installed and configured

## Setup Instructions

### 1. Create an Amazon RDS Database
1. Log in to the AWS Management Console.
2. Navigate to the RDS service.
3. Click on "Create database".
4. Choose "MySQL" as the database engine.
5. Select the "Free tier" template.
6. Configure the database settings:
   - DB instance identifier: `mydb`
   - Master username: `your_username`
   - Master password: `your_password`
7. Click "Create database".
8. Note the **endpoint** and port for later use.
9. Use MysQL Workbench
```bash
create database app_db;
use app_db;
CREATE TABLE users (
id INT AUTO
_
INCREMENT PRIMARY KEY,
username VARCHAR(255) NOT NULL UNIQUE,
password VARCHAR(255) NOT NULL
);
CREATE TABLE uploads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    s3_key VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
### 2. Create an S3 Bucket
1. Navigate to the S3 service in the AWS Management Console.
2. Click on "Create bucket".
3. Enter a unique bucket name (e.g., `my-image-upload-bucket`).
4. Choose the appropriate region.
5. Click "Create bucket".

### 3. Set Up EC2 Instance
1. Navigate to the EC2 service.
2. Click on "Launch Instance".
3. Choose "Ubuntu Server 20.04 LTS".
4. Select the instance type (e.g., `t2.micro`).
5. Configure instance details and add storage as needed.
6. Configure security group to allow inbound traffic on:
   - HTTP (port 80)
   - Custom TCP (port 5000)
   - SSH (port 22)
7. Launch the instance and download the key pair.
8. Make sure has correct IAM role

### 4. Clone the Repository
```bash
git clone https://github.com/your-username/devops-simulation-aws.git
cd devops-simulation-aws
```

### 5. Install Dependencies
SSH into your EC2 instance:
```bash

ssh -i "your-key-pair.pem" ubuntu@your-ec2-public-dns
```
Install required packages:
```bash

sudo apt update
sudo apt install -y python3-pip python3-venv git
```
Set up a virtual environment:
```bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 6. Run the Application
bash

python app.py
Access the application at http://your-ec2-public-dns:5000.
Usage
Navigate to /register to create a new user account.
Navigate to /login to log in.
After logging in, you can upload images to the S3 bucket.
Conclusion
This module demonstrates how to set up a simple web application using Flask, Amazon RDS, and Amazon S3. It provides a foundation for understanding how to integrate AWS services into a web application.
