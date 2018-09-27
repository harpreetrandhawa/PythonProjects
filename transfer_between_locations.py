import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from Scripts.Connection import mysql_server

data = mysql_server('sentinel', 'C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\DXB to KSA.sql')
data1 = mysql_server('sentinel', 'C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\KSA to DXB.sql')

now = datetime.datetime.now()

d = ""
for r in data:
    d = d+""+r[0]+"|"
d = d.rstrip('|')
dd = ""
for r in data1:
    dd = dd+""+r[0]+"|"
dd = dd.rstrip('|')


print 'Sending mail...'
fromaddr = "Proc Team <team.procurement>"
toaddr = ['harpreet.kumar', 'shubham.trivedi','ravi.rupak', 'sanyam.gupta']
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['Subject'] = "Items to be transfer | " + now.strftime("%d %b'%Y %I:%M")
body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p>Please find attached, the files to be tranfer between locations.</p>
            <p><u><B>From DXB to KSA:</b></u><br>""" + d +""" </p>
            <p><u><B>From KSA to DXB:</b></u><br>""" + dd +""" </p>
            <p>Regards,<br>
            Proc reporting</p>
            </body></html> """
msg.attach(MIMEText(body, 'html'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("", "")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
print 'Mail Sent!!!...'
server.quit()
