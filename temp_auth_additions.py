# This file contains the new routes and helper functions to be added to auth.py for forget password functionality.

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from . import mysql

auth = Blueprint('auth', __name__)

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
        reset_link = url_for('auth.reset_password', token=token, _external=True)
        send_password_reset_email(email, reset_link)

        flash('Password reset link sent to your email', 'success')
        return redirect(url_for('auth.login'))

    return render_template('forget_password.html')


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
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
            return redirect(url_for('auth.reset_password', token=token))

        if not is_strong_password(password):
            flash('Password must be at least 8 characters, include uppercase, lowercase, number, and special character.', 'danger')
            return redirect(url_for('auth.reset_password', token=token))

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


import re

def is_strong_password(password):
    # At least 8 chars, one uppercase, one lowercase, one digit, one special char
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[\W_]', password):
        return False
    return True

def send_password_reset_email(to_email, reset_link):
    # Configure your SMTP server details here
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_username = 'your_email@example.com'
    smtp_password = 'your_email_password'

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
