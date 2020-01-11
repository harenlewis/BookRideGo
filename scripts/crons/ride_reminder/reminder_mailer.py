import os
import smtplib
from email.mime.text import MIMEText
from base64 import b64encode, b64decode

def send_mail(request):
    request_json = request.get_json()
    sender = os.environ.get('sender')
    password = os.environ.get('sender')

    receiver = request_json['receiver']
    subject = request_json['subject']
    message = request_json['message']
    
    msg_content = """
    <html>
    <head>
    </head>
    <body>
    <h3>It's time to book an Uber<h3>
    </body>
    </html>
    """

    message = MIMEText(msg_content, 'html')
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    msg_full = message.as_string()

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(sender,password)
        smtpObj.sendmail(sender, receiver.split(","), msg_full)         
        smtpObj.close()
        print("Successfully sent email")

    except Exception:
        print("Error: unable to send email")
