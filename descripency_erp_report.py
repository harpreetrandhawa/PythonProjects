import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from Scripts.Connection import mysql_server
import datetime

# For DXB Report

data = mysql_server('sentinel','C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\epr_desc_dxb.sql','epr_desc_dxb')

now = datetime.datetime.now()

print('Sending mail...')
fromaddr = "Proc Team <team.procurement>"
toaddr = ['shobhit.agrawal','ragini.singh','himanshu.srivastav','owais.nanji ','chitra.lakhani','margi.shah','mubina.badat','ritesh.pande','sankeerth.nadipalli','afiya.mohammed','adegboye.bukola']
tocc = ['shubham.trivedi', 'harpreet.kumar', 'manish.kumar', 'sanyam.gupta']
msg = MIMEMultipart()
 
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['CC'] = ", ".join(tocc)
msg['Subject'] = "ERP discrepancy Master (DXB) | " + now.strftime("%d %b'%Y %I:%M")
 
body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p>Please find attached, list of items in discrepancy due ERP Issues. Please check the list of items to avoid excess procurement.</p>
            <p>Regards,<br>
            Proc Reporting</p>
            </body></html> """
 
msg.attach(MIMEText(body, 'html'))
 
filename = "epr_desc_dxb.csv"

attachment = open("epr_desc_dxb.csv", "r")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("team.procurement", "uloilbojvcaglppz")
text = msg.as_string()
server.sendmail(fromaddr, toaddr+tocc, text)
print('Mail Sent!!!...')
server.quit()

#for KSA Report


data = mysql_server('sentinel','C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\epr_desc_ksa.sql','epr_desc_ksa')

now = datetime.datetime.now()

print('Sending mail...')
fromaddr = "Proc Team <team.procurement>"
toaddr = ['himanshu.srivastav','malik.asif','abdul.rehman','adnan.ali']
tocc = ['shubham.trivedi','harpreet.kumar','manish.kumar', 'sanyam.gupta']
msg = MIMEMultipart()
 
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['CC'] = ", ".join(tocc)
msg['Subject'] = "ERP discrepancy Master (KSA) | " + now.strftime("%d %b'%Y %I:%M")
 
body =""" <html>
            <body>
            <p>Hi Team,</p>
            <p>Please find attached, list of items in discrepancy due ERP Issues. Please check the list of items to avoid excess procurement.</p>
            <p>Regards,<br>
            Proc Reporting</p>
            </body></html> """
 
msg.attach(MIMEText(body, 'html'))
 
filename = "epr_desc_ksa.csv"

attachment = open("epr_desc_ksa.csv", "r")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
msg.attach(part)
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("userid", "password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr+tocc, text)
print('Mail Sent!!!...')
server.quit()
