#/usr/bin/python2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
from Scripts.Connection import mysql_server

now = datetime.datetime.now()

data_dxb = mysql_server('server', "query", 'KSA_inventory')

#"*********************FOR DXB MAIL*******************************"

fromaddr = ""
toaddr = []
tocc = []



now = datetime.datetime.now()
msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['CC'] = ", ".join(tocc)
msg['Subject'] = "Cancellation: DXB Inventory (" + str(len(data_dxb)) + " Items) " + now.strftime("%d %b'%Y %I:%M")

body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p>Please find attached list of """+ str(len(data_dxb)) +""" items which were marked as available in inventory but still not shipped.</p>
            <p>Please get this shipped on priority, as items are coming in cancellation queue.</p>
            <p>Regards,<br>
            Proc reporting</p>
            </body></html> """
msg.attach(MIMEText(body, 'html'))

filename = "DXB_inventory.csv"
attachment = open("DXB_inventory.csv", "r")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('', "")
text = msg.as_string()
server.sendmail(fromaddr, toaddr + tocc, text)
print 'Mail Sent!!!...'
server.quit()


#"*********************FOR KSA MAIL*******************************"

fromaddr = ""
toaddr = []
tocc = []

now = datetime.datetime.now()
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['CC'] = ", ".join(tocc)
msg['Subject'] = "Cancellation: KSA Inventory (" + str(len(data_ksa)) + " Items) " + now.strftime("%d %b'%Y %I:%M")

body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p>Please find attached list of """+ str(len(data_ksa)) +""" items which were marked as available in inventory but still not shipped.</p>
            <p>Please get this shipped on priority, as items are coming in cancellation queue.</p>
            <p>Regards,<br>
            Proc reporting</p>
            </body></html> """
msg.attach(MIMEText(body, 'html'))

filename = "KSA_inventory.csv"
attachment = open("KSA_inventory.csv", "r")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('', "")
text = msg.as_string()
server.sendmail(fromaddr, toaddr + tocc, text)
print 'Mail Sent!!!...'
server.quit()
