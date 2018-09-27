from Scripts.Connection import mysql_server
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime


data = mysql_server('sentinel', "C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\pickr_data_JIT.sql", 'pickr_data_JIT')

headers = ['AWB_number', 'erp_id', 'paymentMethod', 'item_id', 'order_nr','vendor_code','vendor_name','Manager','Driver','pickup_address','Location','destination_city','state','item_discreption','unit_price','qty','recd_qty','is_active','created_date','modified_date','last_update_at','driver','route','newitems','Attempt','flg','status_app','lastremarks','Remarks','comments','Action','dtype','in_scan','out_scan','ready_to_ship_ageing']

df = pd.DataFrame(list(data), columns=headers)

fmile = pd.pivot_table(df, values=['AWB_number'], index=['Location', 'Action'], columns=['Driver'],aggfunc='count',margins=True,margins_name='Grand Total',fill_value='')

not_picked = pd.pivot_table(df.query('Action == ["Not Picked"]'), values=['AWB_number'], index=['Location', 'Remarks'], columns=['Driver'],aggfunc='count', margins=True, margins_name='Grand Total',fill_value='')

table_fmile = fmile.to_html()
table_fmile = table_fmile.replace("AWB_number","No Of Items")
table_fmile = table_fmile.replace('class="dataframe"','class="dataframe" cellspacing = 0 cellpadding = 3')


table_not_picked = not_picked.to_html()
table_not_picked = table_not_picked.replace("AWB_number","Not Picked Items")
table_not_picked = table_not_picked.replace('class="dataframe"','class="dataframe" cellspacing = 0 cellpadding = 3')

fromaddr = "Harpreet Singh <harpreet.kumar>"
toaddr = ['sanyam.gupta']
tocc = ['rahul.chauhan','harpreet.kumar']
#toaddr = 'harpreet.kumar'
#tocc = 'harpreet.kumar'
now = datetime.datetime.now()- datetime.timedelta(1)
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['CC'] = ", ".join(tocc)
msg['Subject'] = "JIT Pickr Report | " + now.strftime("%d %b'%Y")
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
    <p>Please find attach the Pick-up Report for JIT.</p>"""   + table_fmile + """
    <p>Below is the bifurcation for Not Picked Items as per Drivers:</p>""" + table_not_picked + """
    <p>Regards,<br>
    Harpreet Singh<br>
    This is an automated mail. Please contact harpreet.kumar for any query.</p>
    </body></html>"""

msg.attach(MIMEText(body, 'html'))

filename = "pickr_data_JIT.csv"
attachment = open("pickr_data_JIT.csv", "r")
    
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
print 'Picker Report for JIT Mail Sent!!!...'
server.quit()
