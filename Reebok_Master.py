import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import pandas as pd
from Scripts.Connection import mysql_server

data = mysql_server('nm_sourcing', """SELECT item_id, order_nr, exportable_at, rbk.sku, rbk_mod.modelno model_no, rbk.unit_price, order_item_status, rbk.exported_at, (TIMESTAMPDIFF(MINUTE, exportable_at, NOW()) / 60) hour_since, location, IF(po_number = '', 'No', po_number) po_number, CASE WHEN allocated_at != 0 AND shipped_at = 0 THEN 'Allocated'WHEN po_number != ''AND (arrived_at = 0 OR shipped_at = 0) THEN 'PO Created'ELSE 'TP Confirmation'END AS Status, CASE WHEN allocated_at != 0 AND shipped_at = 0 THEN 'No Action (Allocated)'WHEN po_number != ''AND (allocated_at = 0 AND shipped_at = 0) AND TIMESTAMPDIFF(MINUTE, IFNULL(rbk.exportable_at, rbk.exported_at), DATE_ADD(NOW(), INTERVAL 4 HOUR)) > 2160 THEN 'Handover priority 1'WHEN po_number != ''AND (allocated_at = 0 AND shipped_at = 0) AND TIMESTAMPDIFF(MINUTE, IFNULL(rbk.exportable_at, rbk.exported_at), DATE_ADD(NOW(), INTERVAL 4 HOUR)) BETWEEN 1440 AND 2160 THEN 'Handover priority 2'WHEN po_number != ''AND (allocated_at = 0 AND shipped_at = 0) AND TIMESTAMPDIFF(MINUTE, IFNULL(rbk.exportable_at, rbk.exported_at), DATE_ADD(NOW(), INTERVAL 4 HOUR)) <= 1440 THEN 'Handover priority 3'WHEN po_number = ''AND TIMESTAMPDIFF(MINUTE, IFNULL(rbk.exportable_at, rbk.exported_at), DATE_ADD(NOW(), INTERVAL 4 HOUR)) > 3600 THEN 'Hunting'WHEN po_number = ''AND TIMESTAMPDIFF(MINUTE, IFNULL(rbk.exportable_at, rbk.exported_at), DATE_ADD(NOW(), INTERVAL 4 HOUR)) BETWEEN 2160 and 3600 THEN 'TP Confirmation 1'WHEN po_number = ''AND TIMESTAMPDIFF(MINUTE, IFNULL(rbk.exportable_at, rbk.exported_at), DATE_ADD(NOW(), INTERVAL 4 HOUR)) BETWEEN 1440 AND 2160 THEN 'TP Confirmation 2'WHEN po_number = ''AND TIMESTAMPDIFF(MINUTE, IFNULL(rbk.exportable_at, rbk.exported_at), DATE_ADD(NOW(), INTERVAL 4 HOUR)) <= 1440 THEN 'TP Confirmation 3'END Action, IF(vendor_code = '', 'RVEND00001', vendor_code) vendor_code, IF(vendor_name = '', 'R.B.K. Middle East LLC', vendor_name) vendor_name, ROUND(IF(transfer_price = '', paid_price, rbk.transfer_price), 2) transfer_price, if(po_created_at=0,'',po_created_at)po_created_at, if(arrived_at=0,'',arrived_at)arrived_at, if(shipped_at=0,'',shipped_at)shipped_at FROM replica_rbk_sales_order_item_erp rbk LEFT join my_procurement.tbl_rbk_model rbk_mod on rbk_mod.sku = rbk.sku WHERE item_id not in ('AE123','AE124','AE125','AE126','AE127','AE128','AE129','AE133','AE134','AE135','AE137','AE141','AE142','AE143','AE144','AE145','AE146','AE148','AE152','AE153','AE154','AE155','AE156','AE165','AE166','AE167','AE173','AE45','AE46','SA1000','SA1001','SA1003','SA1015','SA543','SA546','SA548','SA549','SA550') and rbk.order_item_status = 'Released'OR (arrived_at != 0 AND shipped_at = 0) group by 1 having Action not in ('No Action (Allocated)');""", 'reebok_master')

headers = ['item_id', 'order_nr', 'exportable_at', 'sku', 'model_no', 'unit_price', 'order_item_status', 'exported_at', 'hour_since', 'location', 'po_number', 'Status', 'Action', 'vendor_code', 'vendor_name', 'transfer_price', 'po_created_at', 'arrived_at', 'shipped_at']

df = pd.DataFrame(list(data), columns=headers)
reebook = pd.pivot_table(df, values=['item_id'], index=['Action'], aggfunc='count', margins=True, margins_name='Total', fill_value='')

tbl_rbk = reebook.to_html()
tbl_rbk = tbl_rbk.replace('class="dataframe"', 'class="dataframe" cellspacing = 0 cellpadding = 3')

fromaddr = "Harpreet Singh <harpreet.kumar>"
toaddr = ['owais.nanji','spandana.vala' , 'bhaswati.bora']
tocc = ['harpreet.kumar', 'sumati.joshi', 'bhaswati.bora', 'sanyam.gupta', 'ravi.rupak']
#toaddr = 'harpreet.kumar'
#tocc = 'harpreet.kumar'
now = datetime.datetime.now()

if now.hour >= 10 and now.hour <= 13:
    run = 'Run 1'
elif now.hour >= 14 and now.hour <= 16:
    run = 'Run 2'
elif now.hour >= 17 and now.hour <= 19:
    run = 'Run 3'
elif now.hour >= 20 and now.hour <= 21:
    run = 'Run 4'
elif now.hour >= 22 and now.hour <= 24:
    run = 'Day Closing'
elif now.hour >= 1 and now.hour <= 2:
    run = 'Day Start'

print run

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['CC'] = ", ".join(tocc)
msg['Subject'] = "Reebook Master Sheet  for " + run + " | " + now.strftime("%d %b'%Y %I:%M")
body = """ <html>
          <head>
          <style>
            table, tr {
            text-align: center;
            font-size:12px;
            width:200px;
            }
            th {
            background-color: #C4DBFF;
            }
            </style>
            </head>
    <body>
    <p>Hi Team,</p>
    <p>Please find attach the Reebook Master Sheet for """ + run + ".</p>"   + tbl_rbk + """
    <p>Regards,<br>
    Harpreet Singh<br>
    This is an automated mail. Please contact harpreet.kumar for any query.</p>
    </body></html>"""

msg.attach(MIMEText(body, 'html'))

filename = "reebok_master.csv"
attachment = open("reebok_master.csv", "r")

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
print 'Reebook Master Sent!!!...'
server.quit()
