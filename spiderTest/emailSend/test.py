import smtplib
from email.mime.text import MIMEText

subject = "Email Subject"
body = "This is the body of the text message"
sender = "oilrobot@outlook.com"  # Your Outlook email address
recipients = ["oilrobot@outlook.com"]  # Recipient email addresses
password = "&G9a.d$m7vU+7hj"  # Your app-specific password

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp_server:
        smtp_server.ehlo()  # Can be omitted
        smtp_server.starttls()  # Secure the connection
        smtp_server.ehlo()  # Can be omitted
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

send_email(subject, body, sender, recipients, password)