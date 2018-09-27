import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import pandas as pd
from Scripts.Connection import mysql_server

data = mysql_server('reporting', "C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\Grocery_Pendings.sql", 'Grocery_pending')
i = 0
while (data == False and i < 5):
    data = mysql_server('reporting', "C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\Grocery_Pendings.sql", 'Grocery_pending')
    i = i + 1

headers = ['itemid', 'order_nr', 'bob_item_status', 'vendor_code', 'vendor_city', 'slot_start', 'slot_end', 'ordered_at', 'exported_at', 'exportable_at', 'shipped_date', 'delivery_date', 'delivered_in_TAT']
df = pd.DataFrame(list(data), columns=headers)

pivot_table = pd.pivot_table(df, values=['itemid', 'shipped_date', 'delivery_date', 'delivered_in_TAT'], index=['vendor_city'], aggfunc='count', fill_value='')
table = pd.DataFrame(pivot_table.to_records())
table.columns = ['vendor_city', 'delivered_in_slot', 'Delivered_Items', 'Confirmed_Items', 'Shipped_Items']
table.sort_values('vendor_city', ascending=True, inplace=True)
table = table[['vendor_city', 'Confirmed_Items', 'Shipped_Items', 'Delivered_Items', 'delivered_in_slot']]
table['confirmed_to_shipped %'] = table['Shipped_Items']/table['Confirmed_Items']*100
table['shipped_to_delivered %'] = table['Delivered_Items']/table['Shipped_Items']*100
table['delivered_in_slot %'] = table['delivered_in_slot']/table['Confirmed_Items']*100
table[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']] = table[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']].apply(lambda x: pd.Series.round(x, 1))
table[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']] = table[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']].astype(str) + " %"
table = table.to_html(index=False)
table = table.replace('class="dataframe"', 'class="dataframe" cellspacing = 0 cellpadding = 3')

pivot_table = pd.pivot_table(df.query('vendor_city == ["Dammam"]'), values=['itemid', 'shipped_date', 'delivery_date', 'delivered_in_TAT'], index=['vendor_city', 'exportable_at'], aggfunc='count', fill_value='')
Dammam = pd.DataFrame(pivot_table.to_records())
Dammam.columns = ['vendor_city', 'Exported_Date', 'delivered_in_slot', 'Delivered_Items', 'Confirmed_Items', 'Shipped_Items']
Dammam.sort_values(['vendor_city', 'Exported_Date'], ascending=[True, False], inplace=True)
Dammam = Dammam[['vendor_city', 'Exported_Date', 'Confirmed_Items', 'Shipped_Items', 'Delivered_Items', 'delivered_in_slot']]
Dammam['confirmed_to_shipped %'] = Dammam['Shipped_Items']/Dammam['Confirmed_Items']*100
Dammam['shipped_to_delivered %'] = Dammam['Delivered_Items']/Dammam['Shipped_Items']*100
Dammam['delivered_in_slot %'] = Dammam['delivered_in_slot']/Dammam['Confirmed_Items']*100
Dammam[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']] = Dammam[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']].apply(lambda x: pd.Series.round(x, 1))
Dammam[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']] = Dammam[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']].astype(str) + " %"
Dammam = Dammam.to_html(index=False)
Dammam = Dammam.replace('class="dataframe"', 'class="dataframe" cellspacing = 0 cellpadding = 3')

pivot_table = pd.pivot_table(df.query('vendor_city == ["Jeddah"]'), values=['itemid', 'shipped_date', 'delivery_date', 'delivered_in_TAT'], index=['vendor_city', 'exportable_at'], aggfunc='count', fill_value='')
Jeddah = pd.DataFrame(pivot_table.to_records())
Jeddah.columns = ['vendor_city', 'Exported_Date', 'delivered_in_slot', 'Delivered_Items', 'Confirmed_Items', 'Shipped_Items']
Jeddah.sort_values(['vendor_city', 'Exported_Date'], ascending=[True, False], inplace=True)
Jeddah = Jeddah[['vendor_city', 'Exported_Date', 'Confirmed_Items', 'Shipped_Items', 'Delivered_Items', 'delivered_in_slot']]
Jeddah['confirmed_to_shipped %'] = Jeddah['Shipped_Items']/Jeddah['Confirmed_Items']*100
Jeddah['shipped_to_delivered %'] = Jeddah['Delivered_Items']/Jeddah['Shipped_Items']*100
Jeddah['delivered_in_slot %'] = Jeddah['delivered_in_slot']/Jeddah['Confirmed_Items']*100
Jeddah[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']] = Jeddah[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']].apply(lambda x: pd.Series.round(x, 1))
Jeddah[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']] = Jeddah[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']].astype(str) + " %"

Jeddah = Jeddah.to_html(index=False)
Jeddah = Jeddah.replace('class="dataframe"', 'class="dataframe" cellspacing = 0 cellpadding = 3')

pivot_table = pd.pivot_table(df.query('vendor_city == ["Riyadh"]'), values=['itemid', 'shipped_date', 'delivery_date', 'delivered_in_TAT'], index=['vendor_city', 'exportable_at'], aggfunc='count', fill_value='')
Riyadh = pd.DataFrame(pivot_table.to_records())
Riyadh.columns = ['vendor_city', 'Exported_Date', 'delivered_in_slot', 'Delivered_Items', 'Confirmed_Items', 'Shipped_Items']
Riyadh.sort_values(['vendor_city', 'Exported_Date'], ascending=[True, False], inplace=True)
Riyadh = Riyadh[['vendor_city', 'Exported_Date', 'Confirmed_Items', 'Shipped_Items', 'Delivered_Items', 'delivered_in_slot']]
Riyadh['confirmed_to_shipped %'] = Riyadh['Shipped_Items']/Riyadh['Confirmed_Items']*100
Riyadh['shipped_to_delivered %'] = Riyadh['Delivered_Items']/Riyadh['Shipped_Items']*100
Riyadh['delivered_in_slot %'] = Riyadh['delivered_in_slot']/Riyadh['Confirmed_Items']*100
Riyadh[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']] = Riyadh[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']].apply(lambda x: pd.Series.round(x, 1))
Riyadh[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']] = Riyadh[['confirmed_to_shipped %', 'shipped_to_delivered %', 'delivered_in_slot %']].astype(str) + " %"

Riyadh = Riyadh.to_html(index=False)
Riyadh = Riyadh.replace('class="dataframe"', 'class="dataframe" cellspacing = 0 cellpadding = 3')



fromaddr = "Harpreet Singh <harpreet.kumar>"
#toaddr = ['daljeet.singh', 'abhijit.banchhor', 'salman.haider', 'manish.kumar', 'categories', 'achyuth.kumar', 'procurement', 'vibhor.khandelwal']
#tocc = ['harpreet.kumar', 'anshul.sharma', 'rahul.chauhan','pratik.gupta']
toaddr = ['pratik.gupta'] #,'ankit.wadhwa', 'eugen.brikcius', 'djamel.mohandoussaid'
tocc = ['rahul.chauhan', 'anshul.sharma', 'ravi.rupak']
now = datetime.datetime.now()- datetime.timedelta(1)
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['CC'] = ", ".join(tocc)
msg['Subject'] = "Grocery MTD | City Wise Data | " + now.strftime("%d %b'%Y")
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
    <p>Hi Pratik,</p>
    <p>Please find below the summary of Grocery Orders, City Wise. Raw data is attached for reference.</p>
    <p>MTD city wise performance:-</p>"""   + table + """
    <p>Day wise performance | Dammam City:-</p>"""   + Dammam + """
    <p>Day wise performance | Jeddah City:-</p>"""   + Jeddah + """
    <p>Day wise performance | Riyadh City:-</p>"""   + Riyadh + """
    <p>Regards,<br>
    Harpreet Singh<br>
    This is an automated mail. Please contact harpreet.kumar for any query.</p>
    </body></html>"""

msg.attach(MIMEText(body, 'html'))

filename = "Grocery_pending.csv"
attachment = open("Grocery_pending.csv", "r")

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
print 'Grocery MTD | City Wise Data Sent!!!...'
server.quit()
