import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
from Scripts.Connection import mysql_server


data = mysql_server('Server', 'file.sql', 'downloadfile')
total = ""

sumbids = 0
sumone = 0
for d in data:
    if d[1]:
        sumbids = sumbids+1
    if d[4] != 0:
        sumone = sumone+1

fromaddr = ""
toaddr = []
tocc = []
now = datetime.datetime.now()
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['CC'] = ", ".join(tocc)
msg['Subject'] = "Ageing | Bin Content"

body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p>Changes found in """ + str(sumone) + """ bids out of """ + str(sumbids) + """ bids.</p>
            <p>Regards,<br>
            Proc reporting</p>
            </body></html> """
msg.attach(MIMEText(body, 'html'))

filename = "ageing_bin_deviation.csv"
attachment = open("ageing_bin_deviation.csv", "r")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('usersID', "Password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr + tocc, text)
print 'Mail Sent!!!...'
server.quit()
