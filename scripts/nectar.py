# general stuff
__user__ = "g-lorenzo"
__date__ = "2020-12-31"
__version__ = "0.1"
__print_flag__ = True

# imports
import time
import datetime
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart

from secret import atble_api, atble_base, email_pass, email_acct, phone
from airtableAPI import ATable

# ----- SECTION 1: Get Information About Today and Access AirTable -----

# Get Today's day of week using datetime, if not Monday (0) or Friday (4), quit
TODAY = datetime.datetime.today().weekday()

# if (TODAY != 0) or (TODAY != 4):
#     quit()

# Create AirTable Class Instance to Access Contacts Table
AT = ATable(api_key=atble_api, base_id=atble_base, table='Contacts')

# ----- SECTION 2: Query AirTable and Return Name Results

# TODO: Update airtableAPI.py to remove duplicates from personal and professional lists

# Use ATable.get_contact_suggestions to get 6 contacts (3 prof, 3 perf)
prof_results = AT.get_contact_suggestions(n=3, pers=False, prof=True)
pers_results = AT.get_contact_suggestions(n=3, pers=True, prof=False)

# Extract Name Information from Results
prof_results = [i['fields']['Name'] for i in prof_results]
pers_results = [i['fields']['Name'] for i in pers_results]

# print results
if __print_flag__:
    print(f"Professional Contacts: {[i for i in prof_results]} ")
    print(f"Personal Contacts: {[i for i in pers_results]} ")

# ----- SECTION 3: Set Up Parameters For SMTP Messaging -----

# SMS Email that Goes to Text where phone is phone number
sms_gateway = f'{phone}@tmomail.net'

# Server and Port to send Email
smtp = "smtp.gmail.com"
port = 587

# 1) Init, Start, and Log In to Email Server
server = smtplib.SMTP(smtp,port)
server.starttls()
server.login(email_acct, email_pass)

# ----- SECTION 4: Place Results into Standard Text Format -----

# Now we use the MIME module to structure our message.
msg = MIMEMultipart()
msg['From'] = email_acct
msg['To'] = sms_gateway

# Make sure you add a new line in the subject
msg['Subject'] = "Build the Well Before You're Thirsty"

# Make sure you also add new lines to your body
body = '\nProfessional Contacts:\n' \
       f'->{prof_results[1]}\n' \
       f'->{prof_results[0]}\n' \
       f'->{prof_results[2]}\n\n' \
       'Personal Contacts:\n' \
       f'->{pers_results[0]}\n' \
       f'->{pers_results[1]}\n' \
       f'->{pers_results[2]}'

# and then attach that body furthermore you can also send html content.
msg.attach(MIMEText(body, 'plain'))
sms = msg.as_string()

# ----- SECTION 5: Send Information to User as Text -----
server.sendmail(email_acct,sms_gateway,sms)

# lastly quit the server
server.quit()


if __name__ == '__main__':
    a = time.time()
    print(f"Hello World! {round(a,2)}")