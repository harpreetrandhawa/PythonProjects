import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from Scripts.Connection import mysql_server


MTD = mysql_server('nm_sourcing', """select
concat(round((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) <=0.5,1,0))/count(1)*100),2),"%") 12Hours,
concat(round((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) <=1,1,0))/count(1)*100),2),"%") 24_hours,
concat(round((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) <=2,1,0))/count(1)*100),2),"%") 48_Hours,
concat(round((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) <=3,1,0))/count(1)*100),2),"%") 72_Hours,
concat(round((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) >3,1,0))/count(1)*100),2),"%") Above_72_Hours
,round(sum(timestampdiff(day,exported_at,arrived_at)-Fridays)/count(1),1)avg_arrival_In_Days1
from (select item_id,
(exportable_at + interval 4 hour)exported_at,
(allocated_at+ interval 4 hour)arrived_at,
floor((dayofweek(date(exportable_at + interval 4 hour)-interval 6 day)+timestampdiff(day,date(exportable_at + interval 4 hour),Date(allocated_at + interval 4 hour)))/7) Fridays
from replica_rbk_sales_order_item_erp rbk

where date(allocated_at + interval 4 hour) >= curdate() - interval day(curdate()-interval 1 day) day 
and date(allocated_at + interval 4 hour) < Curdate())t;""")

Yestrday = mysql_server('nm_sourcing', """select
concat(round(ifnull((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) <=0.5,1,0))/count(1)*100),0),2),"%") 12Hours,
concat(round(ifnull((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) <=1,1,0))/count(1)*100),0),2),"%") 24_hours,
concat(round(ifnull((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) <=2,1,0))/count(1)*100),0),2),"%") 48_Hours,
concat(round(ifnull((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) <=3,1,0))/count(1)*100),0),2),"%") 72_Hours,
concat(round(ifnull((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) >3,1,0))/count(1)*100),0),2),"%") Above_72_Hours
,round(ifnull(sum(timestampdiff(day,exported_at,arrived_at)-Fridays)/count(1),0),1)avg_arrival_In_Days1
from (select item_id,
(exportable_at + interval 4 hour)exported_at,
(allocated_at+ interval 4 hour)arrived_at,
floor((dayofweek(date(exportable_at + interval 4 hour)-interval 6 day)+timestampdiff(day,date(exportable_at + interval 4 hour),Date(allocated_at + interval 4 hour)))/7) Fridays
from replica_rbk_sales_order_item_erp rbk
where date(allocated_at + interval 4 hour) = curdate() - interval 1 day)t;""")

PO_Creation = mysql_server('nm_sourcing', """select
concat(round((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) <=0.5,1,0))/count(1)*100),2),"%") 12Hours,
concat(round((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) <=1,1,0))/count(1)*100),2),"%") 24_hours,
concat(round((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) <=2,1,0))/count(1)*100),2),"%") 48_Hours,
concat(round((sum(if(((timestampdiff(second,t.exported_at,t.arrived_at)/86400) - (Fridays)) >2,1,0))/count(1)*100),2),"%") above_48_Hours
from (select item_id,
(exportable_at + interval 4 hour)exported_at,
(po_created_at+ interval 4 hour)arrived_at,
floor((dayofweek(date(exportable_at + interval 4 hour)-interval 6 day)+timestampdiff(day,date(exportable_at + interval 4 hour),Date(po_created_at + interval 4 hour)))/7) Fridays
from replica_rbk_sales_order_item_erp rbk
where date(po_created_at + interval 4 hour) >= curdate() - interval day(curdate()-interval 1 day) day 
and date(po_created_at + interval 4 hour) < Curdate())t;""")

fromaddr = "Procurement Reporting <team.procurement>"
#toaddr = ['malik.asif', 'adnan.ali', 'abdul.rehman', 'himanshu.srivastav']
#tocc = ['shubham.trivedi', 'harpreet.kumar']
toaddr = ['harpreet.kumar']
tocc = ['harpreet.kumar']
now = datetime.datetime.now()
yest = now - datetime.timedelta(1)
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['CC'] = ", ".join(tocc)
msg['Subject'] = "Reebok Operations " + yest.strftime("%d-%b") + " | MTD in 72 hrs : "+ str(MTD[0][3]) + " | Yesterday in 72 hrs : "+ str(Yestrday[0][3])
body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p>Please find below details regarding this month performance(Reebok):</p>

            <p><b><u>Overall MTD:</u></b></p>
            <table border = 1 cellpadding = 5 cellspacing =0>
            <tr style = "background-color: #afd4ea">
            <th text-align: left >% Arrival(JIT)</th>
            <th text-align: center>Yesterday</th>
            <th text-align: center>MTD</th>
            <th text-align: center>Targets</th>
            </tr><tr><td>12 Hours</td><td>"""+ Yestrday[0][0]+"""</td><td>"""+ MTD[0][0]+"""</td><td>30%</td></tr>
            <tr><td>24 Hours</td><td>"""+ Yestrday[0][1]+"""</td><td>"""+ MTD[0][1]+"""</td><td>50%</td></tr>
            <tr><td>48 Hours</td><td>"""+ Yestrday[0][2]+"""</td><td>"""+ MTD[0][2]+"""</td><td>70%</td></tr>
            <tr><td>72 Hours</td><td>"""+ Yestrday[0][3]+"""</td><td>"""+ MTD[0][3]+"""</td><td>85%</td></tr>
            <tr><td>Above 72 Hours</td><td>"""+ Yestrday[0][4]+"""</td><td>"""+ MTD[0][4]+"""</td><td>85% +</td></tr>
            <tr><td colspan='4'></td></tr>
            <tr><td>Arrival TAT (Days) </td><td>"""+ str(Yestrday[0][5])+"""</td><td>"""+ str(MTD[0][5])+"""</td><td></td></tr>
            </table>

            <p><b><u>PO Creation:</u></b></p>
            <table border = 1 cellpadding = 5 cellspacing =0>
            <tr style = "background-color: #afd4ea">
            <th text-align: left; colspan='2' >% PO Creation</th>
            </tr><tr><td>12 Hours</td><td>"""+ PO_Creation[0][0]+"""</td></tr>
            <tr><td>24 Hours</td><td>"""+ PO_Creation[0][1]+"""</td></tr>
            <tr><td>48 Hours</td><td>"""+ PO_Creation[0][2]+"""</td></tr>
            <tr><td>Above 48 Hours</td><td>"""+ str(PO_Creation[0][2])+"""</td></tr>
            </table>

                       
            <p>Regards,<br>
            Proc reporting</p>
            </body></html> """
msg.attach(MIMEText(body, 'html'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('userid', "password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr + tocc, text)
print 'Mail Sent!!!...'
server.quit()
