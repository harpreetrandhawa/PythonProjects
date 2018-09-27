#/usr/bin/python2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
from Scripts.Connection import mysql_server

now = datetime.datetime.now()

file_data = mysql_server('sentinel', "query", "details")

data = mysql_server("sentinel", "query")

print 'Sending mail...'
fromaddr = ""
toaddr = []
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['Subject'] = "Bifurcation for Items sync time: " + now.strftime("%d %b'%Y %I:%M")
body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p>Please find below, the bifurcation of items sync timing.</p>
            
            <table border = 1 cellpadding = 5 cellspacing =0>
            <tr style = "background-color: #afd4ea">
            <th text-align: left;>Hours</th>
            <th text-align: center># Items</th>
            </tr><tr><td>6 Hrs - 12 Hrs</td><td>"""+ str(data[0][0]) +"""</td></tr>
            <tr><td>12 Hrs - 24 Hrs</td><td>"""+ str(data[0][1]) +"""</td></tr>
            <tr><td>24 Hrs - 48 Hrs</td><td>"""+ str(data[0][2]) +"""</td></tr>
            <tr><td>48 Hrs - 72 Hrs</td><td>"""+ str(data[0][3]) +"""</td></tr>
            <tr><td>Above 72 Hours</td><td>"""+ str(data[0][4]) +"""</td></tr>
            </table>
            
            <p>Regards,<br>
            Proc Reporting</p>
            </body></html>"""
msg.attach(MIMEText(body, 'html'))
filename = "details.csv"

attachment = open("details.csv", "r")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("user", "password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
print 'Mail Sent!!!...'
server.quit()
