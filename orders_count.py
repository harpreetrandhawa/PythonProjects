import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from Scripts.Connection import mysql_server

data = mysql_server("nm_sourcing","""Select sum(if(status = 'exported',1,0))exported,
                    sum(if(status = 'confirmation_pending',1,0))confirmation_pending 
                    from sales_order_item_custom_new;""")
now = datetime.datetime.now()
                    
print 'Sending mail...'
fromaddr = "Proc Team <team.procurement>"
toaddr = ['harpreet.kumar', 'shubham.trivedi', 'ravi.rupak','sanyam.gupta']
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['Subject'] = "Status: Confirmation Pending: "+ str(data[0][1])+ " Items | Exported: "+ str(data[0][0]) +" Items (" + now.strftime("%d %b'%Y %I:%M") +")"
body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p>Please find below, the number of Orders in 'Confirmation_pending' & 'exported' Status.</p>
            <p><u><B>Order in 'exported' Status: </b></u>""" + str(data[0][0]) +""" </p>
            <p><u><B>Order in 'Confirmation_pending' Status: </b></u>""" +str(data[0][1]) +""" </p>
            <p>Regards,<br>
            Proc Reporting</p>
            </body></html>"""
msg.attach(MIMEText(body, 'html'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("user_id", "password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
print 'Mail Sent!!!...'
server.quit()
