import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Scripts.Connection import mysql_server

query = """select sum(wi_bids)to_be_procure,sum(if(ai_stock<=wi_bids,ai_stock,wi_bids))inventory from
(Select wadi_indexer.bids, count(wadi_indexer.bids)wi_bids,ifnull(ai.stock,0)ai_stock
from wadi_indexer 
left join 
(Select bids,count(1)stock from ageing_inventory where bin_type_code = 'PUTPICK' group by bids) ai on ai.bids = wadi_indexer.bids
LEFT OUTER JOIN
erp.order_item_status as erp ON erp.sales_order_item_id = CONCAT(wadi_indexer.db,wadi_indexer.item_id)
where wadi_indexer.vendor_code in (991,995) 
and bob_item_status in ("exportable","exported") 
and erp.pick_line = 'No' 
and erp.pick_registered = 'No' 
group by wadi_indexer.bids)t;"""

data = mysql_server("reporting", query)

fromaddr = "Procurement Reporting <team.procurement>"
toaddr = ['harpreet.kumar', 'shubham.trivedi', 'sanyam.gupta']
msg = MIMEMultipart()
msg['Subject'] = 'Wadi Express Mapped to Retail (' + str(data[0][1]) + ' Items)'
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
content = """<html><body><p>Hi Team</p>
<p>Please find below details regarding items which were tagged to Wadi Express but mapped to JIT vendors.</p>
<table border = 1 cellpadding = 5 cellspacing =0>
<tr style = "background-color: #afd4ea"><th text-align: left>Mapped to Retail</th><th text-align: center>Available</th></tr>
<tr><td text-align: center>"""+ str(data[0][0]) +"""</td><td text-align: center>"""+ str(data[0][1]) +"""</td></tr>
</table>
<P>Regards,</p>
<p>Proc Reporting</p></body></html>"""
msg.attach(MIMEText(content, 'html'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('userid', "password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
print "mail sent!!!"
