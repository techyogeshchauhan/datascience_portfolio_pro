#!/usr/bin/env python3
"""
SMTP Email Backend for Contact Form
Sends emails using Gmail SMTP server
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ============================================
# SMTP CONFIGURATION - UPDATE THESE VALUES
# ============================================

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'sonisharma6102000@gmail.com'
SENDER_PASSWORD = 'mgivlkynzzomxfmu'  # Replace with your Gmail App Password
RECEIVER_EMAIL = 'sonisharma6102000@gmail.com'

# ============================================
# EMAIL SENDING ROUTE
# ============================================

@app.route('/send-email', methods=['POST', 'OPTIONS'])
def send_email():
    # Handle preflight requests
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Get form data
        data = request.form
        
        name = data.get('name', '').strip()
        email = data.get('_replyto', '').strip()
        institution = data.get('institution', '').strip()
        position = data.get('position', '').strip()
        inquiry_type = data.get('inquiryType', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
        response_method = data.get('responseMethod', '').strip()
        phone = data.get('phone', '').strip()
        urgency = data.get('urgency', '').strip()
        
        # Validate required fields
        if not all([name, email, subject, message]):
            return jsonify({
                'success': False,
                'message': 'Please fill all required fields'
            }), 400
        
        # Create email
        msg = MIMEMultipart('alternative')
        msg['From'] = f'Portfolio Contact Form <{SENDER_EMAIL}>'
        msg['To'] = RECEIVER_EMAIL
        msg['Reply-To'] = email
        msg['Subject'] = f'New Contact Form Submission - {subject}'
        
        # HTML email body
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
                .field {{ margin-bottom: 15px; }}
                .label {{ font-weight: bold; color: #667eea; }}
                .value {{ margin-top: 5px; padding: 10px; background: white; border-left: 3px solid #667eea; }}
                .footer {{ background: #333; color: white; padding: 15px; text-align: center; border-radius: 0 0 10px 10px; }}
            </style>
        </head>
        <body>
            <div class='container'>
                <div class='header'>
                    <h2>📧 New Contact Form Submission</h2>
                    <p>You have received a new message from your portfolio website</p>
                </div>
                
                <div class='content'>
                    <div class='field'>
                        <div class='label'>👤 Name:</div>
                        <div class='value'>{name}</div>
                    </div>
                    
                    <div class='field'>
                        <div class='label'>📧 Email:</div>
                        <div class='value'>{email}</div>
                    </div>
                    
                    {f"<div class='field'><div class='label'>🏛️ Institution:</div><div class='value'>{institution}</div></div>" if institution else ""}
                    
                    {f"<div class='field'><div class='label'>💼 Position:</div><div class='value'>{position}</div></div>" if position else ""}
                    
                    {f"<div class='field'><div class='label'>📋 Inquiry Type:</div><div class='value'>{inquiry_type.title()}</div></div>" if inquiry_type else ""}
                    
                    <div class='field'>
                        <div class='label'>📌 Subject:</div>
                        <div class='value'>{subject}</div>
                    </div>
                    
                    <div class='field'>
                        <div class='label'>💬 Message:</div>
                        <div class='value'>{message.replace(chr(10), '<br>')}</div>
                    </div>
                    
                    {f"<div class='field'><div class='label'>📞 Preferred Response:</div><div class='value'>{response_method.title()}</div></div>" if response_method else ""}
                    
                    {f"<div class='field'><div class='label'>☎️ Phone:</div><div class='value'>{phone}</div></div>" if phone else ""}
                    
                    {f"<div class='field'><div class='label'>⚡ Urgency:</div><div class='value'>{urgency.title()}</div></div>" if urgency else ""}
                    
                    <div class='field'>
                        <div class='label'>🕐 Received:</div>
                        <div class='value'>{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
                    </div>
                </div>
                
                <div class='footer'>
                    <p>This email was sent from your portfolio contact form</p>
                    <p><small>Reply directly to this email to respond to {name}</small></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_body = f"""
        New Contact Form Submission
        
        Name: {name}
        Email: {email}
        {f"Institution: {institution}" if institution else ""}
        {f"Position: {position}" if position else ""}
        {f"Inquiry Type: {inquiry_type}" if inquiry_type else ""}
        Subject: {subject}
        
        Message:
        {message}
        
        {f"Preferred Response: {response_method}" if response_method else ""}
        {f"Phone: {phone}" if phone else ""}
        {f"Urgency: {urgency}" if urgency else ""}
        
        Received: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        """
        
        # Attach both versions
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email via Gmail SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        # Success response
        return jsonify({
            'success': True,
            'message': 'Your message has been sent successfully! We will get back to you soon.'
        }), 200
        
    except smtplib.SMTPAuthenticationError:
        return jsonify({
            'success': False,
            'message': 'Email authentication failed. Please check SMTP credentials.'
        }), 500
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Failed to send email. Error: {str(e)}'
        }), 500

# ============================================
# HEALTH CHECK ROUTE
# ============================================

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'Email server is running'
    }), 200

# ============================================
# RUN SERVER
# ============================================

if __name__ == '__main__':
    # For development
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    # For production, use gunicorn:
    # gunicorn -w 4 -b 0.0.0.0:5000 send-email:app
