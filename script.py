import os
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

curr_dir = os.getcwd()
path = curr_dir+'\myfiles'



files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if file:
            files.append(os.path.join(r, file))


for f in files:
    print(f)




message = """Subject: Your grade

Hi {name}, your grade is {grade}"""
from_address = input("Enter Sender Email: ")
password = input("Type your password and press enter: ")

s = smtplib.SMTP('smtp.gmail.com', 587) 

s.starttls() 

s.login(from_address, password)
message = "Message_you_need_to_send"
s.sendmail("sender_email_id", "ravipatel.it@charusat.ac.in", 'Test') 
s.quit() 

"""
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 587, context=context) as server:
    server.login(from_address, password)
    for f in files:
        server.sendmail(
                from_address,
                f,
                message.format(name='Ravi',grade='grade'),
        )
"""
