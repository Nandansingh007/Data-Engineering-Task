import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Read the configuration file
with open('./config.json', 'r') as config_file:
    config = json.load(config_file)

# Retrieve the password from the configuration
smtp_password = config.get('smtp_password')

# Sending emails 
# Standard port and server
smtp_server = "smtp.gmail.com"         # Google server
smtp_port = 587                        # Google Port

#sending and receiver email
from_email = "nandan.singhs007@gmail.com"
to_email = ["nandan.singhsktm@gmail.com","nandan.singhs007@gmail.com"]

smtp_username = "nandan.singhs007@gmail.com"

 
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = ", ".join(to_email)
msg['Subject'] = "Sending Emails with attachment"

csv_filename = "addresses.csv"
# Attach the CSV file to the email
with open('./addresses.csv', 'rb') as attachment:
    part = MIMEApplication(attachment.read(), Name=csv_filename)

part['Content-Disposition'] = f'attachment; filename="{csv_filename}"'
msg.attach(part)

# Connect to the SMTP server and send the email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print("Error sending email:", str(e))

