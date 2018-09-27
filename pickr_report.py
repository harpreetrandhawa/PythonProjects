from Scripts.Connection import mysql_server
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime


data = mysql_server('sentinel', "C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\pickr_data.sql", 'pickr_data')
#print data
headers = ['AWB_number', 'erp_id', 'paymentMethod', 'item_id', 'order_nr', 'vendor_code', 'vendor_name', 'Manager', 'Driver', 'pickup_address', 'Location', 'destination_city', 'state', 'item_discreption', 'unit_price', 'qty', 'recd_qty', 'is_active', 'created_date', 'modified_date', 'last_update_at', 'driver', 'route', 'newitems', 'Attempt', 'flg', 'status_app', 'lastremarks', 'Remarks', 'comments', 'Action', 'dtype', 'in_scan', 'out_scan', 'ready_to_ship_ageing']

df = pd.DataFrame(list(data), columns=headers)

fmile = pd.pivot_table(df, values=['AWB_number'], index=['Location', 'Action'], columns=['Driver'], aggfunc='count', margins=True, margins_name='Grand Total', fill_value='')

not_picked = pd.pivot_table(df.query('Action == ["Not Picked"]'), values=['AWB_number'], index=['Location', 'Remarks'], columns=['Driver'], aggfunc='count', margins=True, margins_name='Grand Total', fill_value='')

table_fmile = fmile.to_html()
table_fmile = table_fmile.replace("AWB_number", "No Of Items")
table_fmile = table_fmile.replace('class="dataframe"', 'class="dataframe" cellspacing = 0 cellpadding = 3')


table_not_picked = not_picked.to_html()
table_not_picked = table_not_picked.replace("AWB_number","Not Picked Items")
table_not_picked = table_not_picked.replace('class="dataframe"','class="dataframe" cellspacing = 0 cellpadding = 3')

fromaddr = "Harpreet Singh <harpreet.kumar>"
toaddr = ['daljeet.singh', 'salman.haider', 'ravi.rupak', 'khalid.abbas', 'jonathan.paulson', 'zohaib.ali', 'jihad.ibrahim']
tocc = [ 'anshul.sharma', 'rahul.chauhan','harpreet.kumar', 'pratik.gupta']
#toaddr = ['anshul.sharma', 'achyuth.kumar']
#tocc = ['harpreet.kumar', 'ravi.rupak']
now = datetime.datetime.now()- datetime.timedelta(1)
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['CC'] = ", ".join(tocc)
msg['Subject'] = "First Mile Pickr Report | " + now.strftime("%d %b'%Y")
body = """ <html>
          <head>
          <style>
            table, tr {
            text-align: center;
            font-size:10px;
            width:1200px;
            }
            th {
            background-color: #D5DBDB;
            }
            </style>
            </head>
    <body>
    <p>Hi Team,</p>
    <p>Please find attach the First Mile Pick-up Report.</p>"""   + table_fmile + """
    <p>Below is the bifurcation for Not Picked Items as per Drivers:</p>""" + table_not_picked + """
    <p>Regards,<br>
    Harpreet Singh<br>
    This is an automated mail. Please contact harpreet.kumar for any query.</p>
    </body></html>"""

msg.attach(MIMEText(body, 'html'))

filename = "pickr_data.csv"
attachment = open("pickr_data.csv", "r")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('userid', "password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr + tocc, text)
print 'Picker Report Mail Sent!!!...'
server.quit()

# FOR READY_TO_SHIP REPORT

pd.options.display.float_format = '{:,.0f}'.format

RTS = pd.pivot_table(df.query('Action == ["Not Picked", "Not Attempted"]'), values=['AWB_number'], index=['Manager'], columns=['ready_to_ship_ageing'], aggfunc='count', margins=True, margins_name='Total', fill_value='')

RTS = pd.DataFrame(RTS.to_records())

RTS.columns = ['Manager','0-1 Day','1-2 Day','2-3 Day', '3+ Day', 'Total']

RTS = RTS.sort_values('Total', ascending=False)
RTS = RTS.apply(pd.to_numeric,errors= 'ignore')
RTS = RTS.fillna(0)

RTS['Over TAT(%)'] = ((RTS['1-2 Day']) + (RTS['2-3 Day']) + (RTS['3+ Day']))/(RTS['Total']) * 100

RTS = RTS.round({'Over TAT(%)':1})
RTS['Over TAT(%)'] = RTS['Over TAT(%)'].astype(str) + " %"
    
table_RTS = RTS.to_html(index=False)
table_RTS = table_RTS.replace("AWB_number","No Of Items")
table_RTS = table_RTS.replace('class="dataframe"','class="dataframe" cellspacing = 0 cellpadding = 3')

fromaddr = "Harpreet Singh <harpreet.kumar>"
#toaddr = ['daljeet.singh', 'abhijit.banchhor', 'salman.haider', 'manish.kumar', 'categories', 'achyuth.kumar', 'procurement', 'vibhor.khandelwal']
#tocc = ['harpreet.kumar', 'anshul.sharma', 'rahul.chauhan','pratik.gupta']
toaddr = ['anshul.sharma', 'jonathan.paulson']
tocc = ['harpreet.kumar', 'ravi.rupak']
now = datetime.datetime.now()- datetime.timedelta(1)
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['CC'] = ", ".join(tocc)
msg['Subject'] = "Marketplace Orders In Ready to ship status pending for Handover | " + now.strftime("%d %b'%Y")
body = """ <html>
          <head>
          <style>
            table, tr {
            text-align: center;
            font-size:10px;
            width:500px;
            }
            th {
            background-color: #D5DBDB;
            }
            </style>
            </head>
    <body>
    <p>Hi Team,</p>
    <p>Following orders are pending for Handover. Request you to check with the sellers and make sure these orders are handed over to drivers today itself. 
In case seller wants to cancel these orders please upload the details in shared <a href="https://docs.google.com/spreadsheets/d/1boZAgTERy2_IaL-dMdIe5yDyHkUen8SvA5Qkfb5oNu0/edit#gid=0">Cancellation Sheet</a>.</p>"""   + table_RTS + """
    <p>Regards,<br>
    Harpreet Singh<br>
    This is an automated mail. Please contact harpreet.kumar for any query.</p>
    </body></html>"""

msg.attach(MIMEText(body, 'html'))

filename = "pickr_data.csv"
attachment = open("pickr_data.csv", "r")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('userid', "password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr + tocc, text)
print 'RTS Mail Sent!!!...'
server.quit()
