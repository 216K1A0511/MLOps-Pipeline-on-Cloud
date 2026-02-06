import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_email_alert(subject, body, to_email):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    
    if not sender_email or not sender_password:
        print("Error: EMAIL_USER or EMAIL_PASS environment variables not set.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Using Gmail's SMTP server by default
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    # Example usage
    subject = f"MLOps Pipeline Alert - {datetime.now().strftime('%Y-%m-%d')}"
    body = "The MLOps pipeline has completed a run. Please check the reports folder for details."
    # Replace with your recipient
    recipient = "your_email@example.com" 
    
    send_email_alert(subject, body, recipient)
