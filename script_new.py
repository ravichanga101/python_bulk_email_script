import smtplib
import os
import time
import getpass
import sys
import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def check(email):  
  
    # pass the regualar expression 
    # and the string in search() method 
    if(re.search(regex,email)):  
        return True  
          
    else:  
        return False



arguments = sys.argv[1:]
count = len(arguments)
if count <= 0:
    curr_dir = os.getcwd()
    path = curr_dir+'\myfiles'
    
else :
    path = arguments[0] # full path
    
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if file:
            files.append(os.path.join(r, file))

from_address = input("Enter Sender Email: ")
password = getpass.getpass(prompt='Type your password and press enter: ') 

# Create message container - the correct MIME type is multipart/alternative.


# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?({email})<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

s = smtplib.SMTP('smtp.gmail.com', 587) 
s.starttls() 
s.login(from_address, password)

for f in files:
    print(f)
    head, tail = os.path.split(f)
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link Test"
    msg['From'] = from_address
    msg['To'] = tail
    
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html.format(email=tail), 'html')

    filename = tail
    attachment = open(f, "rb")

    part3 = MIMEBase('application', 'octet-stream')
    part3.set_payload((attachment).read())
    encoders.encode_base64(part3)
    part3.add_header('Content-Disposition', "attachment; filename= {fname}".format(fname=filename))

    msg.attach(part1)
    msg.attach(part2)
    msg.attach(part3)

    time.sleep(1)
    if check(tail) :
        s.sendmail(from_address, tail, msg.as_string())
    else :
        print(tail+' Invalid Email')
        continue

    print(tail+' Sent')

s.quit()