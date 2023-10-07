import mysql.connector
import pandas as pd
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


# Read the configuration file
with open('/mnt/c/Users/Nandan/Onedrive/Desktop/task/config.json', 'r') as config_file:
    config = json.load(config_file)

# Retrieve the password from the configuration
mysql_password = config.get('mysql_password')

try:
    
    # Create a connection to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="sakila"
    )

    # Check if the connection is successful
    if db.is_connected():
        print("Connected to the database successfully")

    # Perform a simple operation
    cursor = db.cursor()
    
    #SQL query to fetch new rentals in the last 1 hour
    query = """
                SELECT
                r.rental_id,
                r.rental_date,
                CONCAT(cu.first_name, " ", cu.last_name) AS Name,
                f.title,
                c.country AS Country_Country
            FROM
                rental r
            INNER JOIN
                customer cu ON r.customer_id = cu.customer_id
            INNER JOIN
                inventory i ON r.inventory_id = i.inventory_id
            INNER JOIN
                film f ON i.film_id = f.film_id
            INNER JOIN
                address a ON cu.address_id = a.address_id
            INNER JOIN
                city ci ON a.city_id = ci.city_id
            INNER JOIN
                country c ON ci.country_id = c.country_id
            WHERE
                r.rental_date>=NOW() - INTERVAL 1 HOUR;
    """
    # Execute the query and fetch the results
    cursor.execute(query)
    result = cursor.fetchall()

    # Create a DataFrame from the query result
    df = pd.DataFrame(result, columns=["rental_id", "rental_date", "Customer Name", "Film_title", "Country Name"])

    # Create a CSV file from the DataFrame
    csv_filename = "new_rentals.csv"
    df.to_csv(csv_filename, index=False)

   
    # Close the database connection
    db.close()
    print("Database connection closed")

except mysql.connector.Error as err:
    print("Error:", err)
    

# Sending emails 
# Standard port and server
smtp_server = "smtp.gmail.com"         # Google server
smtp_port = 587                        # Google Port

#sending and receiver email
from_email = "nandan.singhs007@gmail.com"
to_email = ["nandan.singhsktm@gmail.com","nandan.singhs007@gmail.com"]



# Read the configuration file
with open('/mnt/c/Users/Nandan/Onedrive/Desktop/task/config.json', 'r') as config_file:
    config = json.load(config_file)

# Retrieve the password from the configuration
smtp_password = config.get('smtp_password')
smtp_username = "nandan.singhs007@gmail.com"

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = ", ".join(to_email)
msg['Subject'] = "New Rentals in the Last Hour"

csv_filename = "new_rentals.csv"

# Attach the CSV file to the email
with open('/mnt/c/Users/Nandan/Onedrive/Desktop/task/new_rentals.csv', 'rb') as attachment:
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

