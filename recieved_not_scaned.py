import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import pandas as pd
from Scripts.Connection import mysql_server


data = mysql_server('sentinel', """select itemid,order_nr,erpid,recd_qty,skucode as awb,vendor_code,
vendor_name,country,modified_date,pickup_date as picked_at,status_app,in_scan,out_scan, driver,
date(pickup_date)pickup_date,
if(status_app = 'mp_cancel','Cancelled',if(status_app not in ('picked','expired'),'Shipped','Not Scanned'))carrier_comment

from tbl_lightbox_pickr_details where recd_qty =1 and in_scan =0 and dtype ='dropship';""", 'recd_not_scaned')

headers = ['itemid', 'order_nr', 'erpid', 'recd_qty', 'awb', 'vendor_code', 'vendor_name', 'country', 'modified_date', 'picked_at', 'status_app', 'in_scan', 'out_scan', 'driver', 'pickup_date', 'carrier_comment']

df = pd.DataFrame(list(data), columns=headers)

df['pickup_date'] = pd.to_datetime(df['pickup_date'], format='%Y-%m-%d')

ptable = pd.pivot_table(df, values=['itemid'], index=['pickup_date'], columns=['carrier_comment'], aggfunc='count', fill_value=0)
print ptable

ptable = pd.DataFrame(ptable.to_records())
ptable.columns = ['Date', 'Cancelled', 'Not Scanned', 'Shipped']
ptable['Date'] = pd.to_datetime(ptable['Date'], format='%Y-%m-%d')
ptable = ptable.sort_values('Date', ascending=False)
ptable = ptable.head(15)

ptable['Grand Total'] = ptable['Not Scanned'] + ptable['Cancelled'] + ptable['Shipped']

#ptable.loc['Total'] = ['',ptable['Cancelled'].sum(), ptable['Not Scanned'].sum(), ptable['Shipped'].sum(), ptable['Grand Total'].sum()]

table_ptable = ptable.to_html(index=False)
table_ptable = table_ptable.replace('class="dataframe"', 'class="dataframe" cellspacing = 0 cellpadding = 3')

fromaddr = "Harpreet Singh <harpreet.kumar>"
toaddr = ['anshul.sharma', 'rahul.chauhan', 'daljeet.singh', 'sanyam.gupta', 'salman.haider', 'khalid.abbas', 'sellercaremembers', 'jihad.ibrahim']
tocc = ['harpreet.kumar', 'ravi.rupak']

#toaddr = ['harpreet.kumar']
#tocc = ['ravi.rupak']

now = datetime.datetime.now()
msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['CC'] = ", ".join(tocc)
msg['Subject'] = "Items Picked But not scan | MarketPlace: "  + "(" + now.strftime("%d %b'%Y %I:%M") +")"

body = """ <html>
          <head>
          <style>
            table, tr {
            text-align: center;
            font-size:10px;
            width:500px;
            }
            th {
            text-align: center;
            background-color: #D5DBDB;
            }
            </style>
            </head>
            <body>
            <p>Hi Team,</p>
            <p>Please find attached details which are picked by the drivers but not scaned yet.</p>
            <p>Below Are the summary for last 15 Days.</p>"""   + table_ptable + """
            <p>Regards,<br>
            Harpreet Singh</p>
            </body></html> """
msg.attach(MIMEText(body, 'html'))

filename = "recd_not_scaned.csv"
attachment = open("recd_not_scaned.csv", "r")
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
print 'Mail Sent!!!...'
server.quit()
