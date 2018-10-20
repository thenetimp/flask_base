import smtplib
from flask import render_template, url_for, current_app as app
from flask_login import current_user
 

def send_password_reset_token(dest_email_address, reset_token):
    site_host = app.config['SITE_HOST']
    message = render_template('v1/email/user/password_token.html', site_host=site_host, reset_token=reset_token)
    send_email_message('thenetimp@gmail.com', dest_email_address, message)
    

def send_email_message(dest_email_address, subject, message=""):
    print(app.config['SMTP_USER'])
    print(app.config['SMTP_PASSWORD'])
    server = smtplib.SMTP(app.config['SMTP_HOST'], app.config['SMTP_PORT'])
    server.starttls()
    server.login(app.config['SMTP_USER'], app.config['SMTP_PASSWORD'])
    server.sendmail(app.config['SRC_EMAIL_ADDRESS'], dest_email_address, message)
    server.quit()