from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import mysql
import re
import secrets
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from werkzeug.security import generate_password_hash, check_password_hash
import random
import time

auth = Blueprint('auth', __name__)

def is_strong_password(password):
    # Password must be at least 8 characters, include uppercase, lowercase, number, and special character
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

# New route: forgot-password
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        identifier = request.form.get('identifier')  # email or phone
        if not identifier:
            flash('Please enter your email or phone number', 'danger')
            return redirect(url_for('auth.forgot_password'))

        cursor = mysql.connection.cursor()
        # Check if identifier is email or phone number
        is_email = re.match(r"[^@]+@[^@]+\.[^@]+", identifier)
        user = None
        if is_email:
            cursor.execute("SELECT email FROM jobseeker WHERE email = %s", (identifier,))
            user = cursor.fetchone()
            if not user:
                cursor.execute("SELECT email FROM jobpublisher WHERE email = %s", (identifier,))
                user = cursor.fetchone()
        else:
            cursor.execute("SELECT phoneNumber FROM jobseeker WHERE phoneNumber = %s", (identifier,))
            user = cursor.fetchone()
            if not user:
                cursor.execute("SELECT phoneNumber FROM jobpublisher WHERE phoneNumber = %s", (identifier,))
                user = cursor.fetchone()
        cursor.close()

        if not user:
            flash('Email or phone number not found', 'danger')
            return redirect(url_for('auth.forgot_password'))

        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        session['otp'] = otp
        session['otp_expiry'] = time.time() + 300  # OTP valid for 5 minutes
        session['identifier'] = identifier

        # Send OTP via email (and optionally SMS)
        if is_email:
            send_otp_email(identifier, otp)
        else:
            send_otp_sms(identifier, otp)  # Optional: implement or stub

        flash('OTP sent to your email or phone. Please verify.', 'info')
        return redirect(url_for('auth.verify_otp'))

    return render_template('forgot_password.html')

# New route: verify OTP
@auth.route('/verify', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        if not entered_otp:
            flash('Please enter the OTP', 'danger')
            return redirect(url_for('auth.verify_otp'))

        if 'otp' not in session or 'otp_expiry' not in session or 'identifier' not in session:
            flash('Session expired or invalid. Please start over.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        if time.time() > session['otp_expiry']:
            session.pop('otp', None)
            session.pop('otp_expiry', None)
            session.pop('identifier', None)
            flash('OTP expired. Please request a new one.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        if entered_otp != session['otp']:
            flash('Incorrect OTP. Please try again.', 'danger')
            return redirect(url_for('auth.verify_otp'))

        # OTP verified
        session['otp_verified'] = True
        flash('OTP verified. Please reset your password.', 'success')
        return redirect(url_for('auth.reset_password_otp'))


    return render_template('verify.html')

# New route: reset password
@auth.route('/reset-password-otp', methods=['GET', 'POST'])
def reset_password_otp():
    if 'otp_verified' not in session or not session['otp_verified']:
        flash('Unauthorized access. Please verify OTP first.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        repeat_password = request.form.get('repeatPassword')

        if not password or not repeat_password:
            flash('Please fill all password fields', 'danger')
            return redirect(url_for('auth.reset_password_otp'))

        if password != repeat_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.reset_password_otp'))

        if not is_strong_password(password):
            flash('Password must be at least 8 characters, include uppercase, lowercase, number, and special character.', 'danger')
            return redirect(url_for('auth.reset_password_otp'))

        identifier = session.get('identifier')
        if not identifier:
            flash('Session expired. Please start over.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        cursor = mysql.connection.cursor()
        is_email = re.match(r"[^@]+@[^@]+\.[^@]+", identifier)
        if is_email:
            cursor.execute("UPDATE jobseeker SET password = %s WHERE email = %s", (password, identifier))
            cursor.execute("UPDATE jobpublisher SET password = %s WHERE email = %s", (password, identifier))
        else:
            cursor.execute("UPDATE jobseeker SET password = %s WHERE phoneNumber = %s", (password, identifier))
            cursor.execute("UPDATE jobpublisher SET password = %s WHERE phoneNumber = %s", (password, identifier))
        mysql.connection.commit()
        cursor.close()

        # Clear session data related to OTP
        session.pop('otp', None)
        session.pop('otp_expiry', None)
        session.pop('identifier', None)
        session.pop('otp_verified', None)

        flash('Password reset successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')

# Helper function to send OTP email
def send_otp_email(to_email, otp):
    import os
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.getenv('GMAIL_USERNAME')
    smtp_password = os.getenv('GMAIL_PASSWORD')

    if not smtp_username or not smtp_password:
        print("GMAIL_USERNAME and GMAIL_PASSWORD environment variables must be set")
        return

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = 'Your OTP for Password Reset'

    body = f"Your OTP for password reset is: {otp}. It is valid for 5 minutes."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Stub for sending OTP SMS via Twilio (optional)
def send_otp_sms(phone_number, otp):
    # Implement Twilio SMS sending here or leave as stub
    print(f"Sending OTP {otp} to phone number {phone_number} (SMS sending not implemented)")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        # Try login as Seeker
        cur.execute("SELECT seekerID, fname, password FROM jobseeker WHERE email = %s", (email,))
        seeker = cur.fetchone()

        if seeker:
            seeker_id, seeker_fname, seeker_password = seeker
            if seeker_password == password:
                session['user_id'] = seeker_id
                session['role'] = 'seeker'
                session['basic_info'] = {'first_name': seeker_fname} 
                flash("Login successful as Job Seeker!", "success")
                cur.close()
                return redirect(url_for('views.seekerdashboard'))

        # Try login as Publisher
        cur.execute("SELECT publisherID, fname, password FROM jobpublisher WHERE email = %s", (email,))
        publisher = cur.fetchone()
        cur.close()

        if publisher:
            publisher_id, publisher_fname, publisher_password = publisher
            if publisher_password == password:
                session['user_id'] = publisher_id
                session['role'] = 'publisher'
                session['basic_info'] = {'first_name': publisher_fname}
                flash("Login successful as Publisher!", "success")
                return redirect(url_for('views.publisher_dashboard'))

        flash("Invalid email or password.", "danger")
        return redirect(url_for('auth.login'))
    
    return render_template("login.html")


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Add form validation
        required_fields = ['firstName', 'lastName', 'email', 'password', 'role']
        if not all(field in request.form for field in required_fields):
            flash('Please fill all required fields', 'danger')
            return redirect(url_for('auth.signup'))

        password = request.form.get('password')
        repeat_password = request.form.get('repeatPassword')

        if password != repeat_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.signup'))

        if not is_strong_password(password):
            flash('Password must be at least 8 characters, include uppercase, lowercase, number, and special character.', 'danger')
            return redirect(url_for('auth.signup'))
        email = request.form.get('email')
        cur = mysql.connection.cursor()

        # Check if email exists in jobseeker table
        cur.execute("SELECT email FROM jobseeker WHERE email = %s", (email,))
        seeker_email = cur.fetchone()

        # Check if email exists in jobpublisher table
        cur.execute("SELECT email FROM jobpublisher WHERE email = %s", (email,))
        publisher_email = cur.fetchone()
        cur.close()

        if seeker_email or publisher_email:
            flash('Email already exists. Please use a different email or login.', 'danger')
            return redirect(url_for('auth.signup'))
        # Store in session
        session['basic_info'] = {
            'first_name': request.form.get('firstName'),
            'last_name': request.form.get('lastName'),
            'email': request.form.get('email'),
            'password': password,
            'role': request.form.get('role')
        }

        # Verify role selection
        role = request.form.get('role')
        if role == 'seeker':
            return redirect(url_for('auth.seeker_info'))
        elif role == 'publisher':
            return redirect(url_for('auth.publisher_info'))
        
        flash('Invalid role selection', 'danger')
        return redirect(url_for('auth.signup'))

    return render_template('signup.html')


@auth.route('/seekerinfo', methods=['GET', 'POST'])
def seeker_info():
    if request.method == 'POST':
        try:
            if 'basic_info' not in session:
                flash("Session expired. Please start over.", 'danger')
                return redirect(url_for('auth.signup'))

            # Validate file upload
            if 'document' not in request.files:
                flash('Document is required', 'danger')
                return redirect(request.url)
            
            file = request.files['document']
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)

            # Get form data
            phone = request.form.get('phone')
            address = request.form.get('address')
            city = request.form.get('city')
            country = request.form.get('country')
            gender = request.form.get('gender')
            disability_type = request.form.get('disabilityType')
            document_data = file.read()

            # Get session data
            basic_info = session['basic_info']
            
            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO jobseeker 
                (fname, lname, email, password, phoneNumber, address, city, country, gender, disability_type, disabilitydocument)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                basic_info['first_name'],
                basic_info['last_name'],
                basic_info['email'],
                basic_info['password'],  # Hashed password
                phone,
                address,
                city,
                country,
                gender,
                disability_type,
                document_data
            ))
            
            mysql.connection.commit()
            user_id = cursor.lastrowid
            cursor.close()

            session['user_id'] = user_id
            session['role'] = 'seeker'
            session.pop('basic_info', None)

            flash('Registration successful!', 'success')
            return redirect(url_for('views.seekerdashboard'))

        except Exception as e:
            mysql.connection.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
            return redirect(url_for('auth.signup'))

    return render_template('seekerinfo.html')


@auth.route('/publisherinfo', methods=['GET', 'POST'])
def publisher_info():
    if request.method == 'POST':
        if 'basic_info' not in session:
            flash("Please complete signup first.", 'danger')
            return redirect(url_for('auth.signup'))

        # Extract form data
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        country = request.form.get('country')
        gender = request.form.get('gender')

        fname = session['basic_info']['first_name']
        lname = session['basic_info']['last_name']
        email = session['basic_info']['email']
        password = session['basic_info']['password']

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO jobpublisher (fname, lname, email, password, phoneNumber, address, city, country, gender)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (fname, lname, email, password, phone, address, city, country, gender))

        mysql.connection.commit()

        session['user_id'] = cursor.lastrowid
        session['role'] = 'publisher'
        session.pop('basic_info', None)

        cursor.close()

        flash("Publisher registration complete!", "success")
        return redirect(url_for('views.publisher_dashboard'))

    return render_template('publisherinfo.html')


# New routes for forget password functionality

@auth.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash('Please enter your email address', 'danger')
            return redirect(url_for('auth.forget_password'))

        cursor = mysql.connection.cursor()
        # Check if email exists in jobseeker or jobpublisher
        cursor.execute("SELECT seekerID FROM jobseeker WHERE email = %s", (email,))
        seeker = cursor.fetchone()
        cursor.execute("SELECT publisherID FROM jobpublisher WHERE email = %s", (email,))
        publisher = cursor.fetchone()

        if not seeker and not publisher:
            flash('Email address not found', 'danger')
            cursor.close()
            return redirect(url_for('auth.forget_password'))

        # Generate token and expiry (1 hour)
        token = secrets.token_urlsafe(32)
        expiry = datetime.utcnow() + timedelta(hours=1)

        # Store token and expiry in a password_resets table (create if not exists)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_resets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                token VARCHAR(255) NOT NULL,
                expires_at DATETIME NOT NULL
            )
        """)
        cursor.execute("DELETE FROM password_resets WHERE email = %s", (email,))
        cursor.execute("INSERT INTO password_resets (email, token, expires_at) VALUES (%s, %s, %s)", (email, token, expiry))
        mysql.connection.commit()
        cursor.close()

        # Send email with reset link
        reset_link = url_for('auth.reset_password_token', token=token, _external=True)
        send_password_reset_email(email, reset_link)

        flash('Password reset link sent to your email', 'success')
        return redirect(url_for('auth.login'))

    return render_template('forget_password.html')


@auth.route('/reset_password/<token>', methods=['GET', 'POST'], endpoint='reset_password_token')
def reset_password_token(token):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT email, expires_at FROM password_resets WHERE token = %s", (token,))
    record = cursor.fetchone()

    if not record:
        flash('Invalid or expired token', 'danger')
        cursor.close()
        return redirect(url_for('auth.login'))

    email, expires_at = record
    if expires_at < datetime.utcnow():
        flash('Token expired', 'danger')
        cursor.execute("DELETE FROM password_resets WHERE token = %s", (token,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        password = request.form.get('password')
        repeat_password = request.form.get('repeatPassword')

        if password != repeat_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.reset_password_token', token=token))

        if not is_strong_password(password):
            flash('Password must be at least 8 characters, include uppercase, lowercase, number, and special character.', 'danger')
            return redirect(url_for('auth.reset_password_token', token=token))

        # Update password in jobseeker or jobpublisher
        if is_seeker_email(email):
            cursor.execute("UPDATE jobseeker SET password = %s WHERE email = %s", (password, email))
        else:
            cursor.execute("UPDATE jobpublisher SET password = %s WHERE email = %s", (password, email))

        cursor.execute("DELETE FROM password_resets WHERE token = %s", (token,))
        mysql.connection.commit()
        cursor.close()

        flash('Password reset successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    cursor.close()
    return render_template('reset_password.html', token=token)


def is_seeker_email(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT seekerID FROM jobseeker WHERE email = %s", (email,))
    seeker = cursor.fetchone()
    cursor.close()
    return seeker is not None


import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_password_reset_email(to_email, reset_link):
    # Configure your SMTP server details here using environment variables for security
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.getenv('GMAIL_USERNAME')
    smtp_password = os.getenv('GMAIL_PASSWORD')

    if not smtp_username or not smtp_password:
        print("GMAIL_USERNAME and GMAIL_PASSWORD environment variables must be set")
        return

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = 'Password Reset Request'

    body = f"Please click the following link to reset your password:\n\n{reset_link}\n\nIf you did not request this, please ignore this email."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
