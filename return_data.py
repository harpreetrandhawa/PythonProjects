import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
from Scripts.Connection import mysql_server

query = """ """

data = mysql_server("reporting", query, 'Returns Details')
now = datetime.datetime.now()
query = """ """

data1 = mysql_server("sentinel", query, 'Third Scan')
now = datetime.datetime.now()

fromaddr = "Proc Team <team.procurement>"
toaddr = ['ravi.rupak']
msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['Subject'] = " Returns Details | " + now.strftime("%d %b'%Y %I:%M")

body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p>Please find attached, list of Shipped Orders for Marketplace.</p>
            <p>Regards,<br>
            Proc Reporting</p>
            </body></html> """

msg.attach(MIMEText(body, 'html'))

filename = "Returns_data.csv"

attachment = open("Returns_data.csv", "r")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("userid", "password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
print 'Mail Sent!!!...'
server.quit()
