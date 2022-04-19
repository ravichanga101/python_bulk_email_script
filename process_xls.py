import smtplib
import os
import time
import getpass
import sys
import xlrd 
import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

import csv

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def check(email):  
    # pass the regualar expression 
    # and the string in search() method 
    if(re.search(regex,email)):  
        return True  
    else:  
        return False

curr_dir = os.getcwd()

loc = ("CSIRSC_2020_9.xlsx") 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 

#print(sheet.nrows)
#print(sheet.ncols)

csv_file = open('sent_report.csv', 'a', newline='') 
writer = csv.writer(csv_file)

#from_address = input("Enter Sender Email: ")
#password = getpass.getpass(prompt='Type your password and press enter: ') 

from_address = "csirsc2020.noreply2@charusat.ac.in"
password = "ecchanga"

html = """\
<html>
  <head></head>
  <body>
    <h3>Greetings !!! <br></h3>    
    <h4>Thank you, for participating in CSIRSC-2020.</h4>
    <h4>You are heartily welcome to the CHARUSAT. You are requested to remain present for the registration at 9.00 a.m. 24/25-Jan-2020, Central Lawn, CHARUSAT.</h4>
    
    <h4><u>Kindly present the attached QR-CODE for registration.</u></h4>
    <h4><u>Your Registration Details:</u></h4>
    <div>   
       <h4>Candidate Name : {name}</h4>
       <h4>Event Name : {event_name}</h4>
       <h4>For More Information and Event Schedule visit Website: https://www.charusat.ac.in/csirsc2020/ </h4>
    </div>
    
    <h4>This is auto-generated mail, please do not reply.</h4>
    <div>
    <h4>Regards</h4>
    <span>
    Team CSIRSC-2020<br>
    CHARUSAT,Changa<br>
    https://www.charusat.ac.in/
    </span>
    <div>

  </body>
</html>
"""

s = smtplib.SMTP('smtp.gmail.com', 587) 
s.starttls() 
s.login(from_address, password)


for i in range (0, 101):
    
    try:
        # sr_no = sheet.cell_value(i, 0)
        print(i)
        candi_name = sheet.cell_value(i, 0)
        event = sheet.cell_value(i, 1)
        email_to_send = sheet.cell_value(i, 4)
        qr_code_png = sheet.cell_value(i, 8)

        print(qr_code_png)
    
        if check(email_to_send) == False:
            print(email_to_send+' Invalid Email')
            continue
            

        msg = MIMEMultipart()
        msg['Subject'] = "Registration Details - CSIRSC-2020 at CHARUSAT"
        msg['From'] = from_address
        msg['To'] = email_to_send
        
        
        part2 = MIMEText(html.format(email=email_to_send,event_name=event,name=candi_name), 'html')

        
        msg.attach(part2)

        #filename = email_to_send
        filename = qr_code_png
        path_to_folder = curr_dir+'\qr_codes\\'+filename+'.png'
        
        if os.path.exists(path_to_folder) :
         
            
            part = MIMEBase('application', "octet-stream")
            part.set_payload( open(path_to_folder,"rb").read() )
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(path_to_folder))
            msg.attach(part)
            
            """   
            part = MIMEBase('application', "octet-stream")
            part.set_payload( open("CSI_Event_Schedule.pdf","rb").read() )
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % "CSI_Event_Schedule.pdf")
            msg.attach(part)
            """
            
            '''
            attachment = open(path_to_folder, "rb")

            part3 = MIMEBase('application', 'octet-stream')
            part3.set_payload((attachment).read())
            encoders.encode_base64(part3)
            part3.add_header('Content-Disposition', "attachment; filename= {fname}".format(fname=filename))
            msg.attach(part3)

            attachment1 = open("CSI_Event_Schedule.pdf", "rb")

            part4 = MIMEBase('application', 'octet-stream')
            part4.set_payload((attachment1).read())
            encoders.encode_base64(part4)
            part4.add_header('Content-Disposition', "attachment; filename= {fname}".format(fname="CSI_Event_Schedule.pdf"))
            msg.attach(part4)
            '''
        # time.sleep(1)
        s.sendmail(from_address, email_to_send, msg.as_string())
        writer.writerow([candi_name, email_to_send,"Sent"])
    except Exception as e:
        writer.writerow([candi_name, email_to_send,"NOT SENT-ERROR!"])
        print(e)
        continue
            
    
csv_file.close()
s.quit()