import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
from Scripts.Connection import mysql_server

print 'Sending Zendesk_Tags/Cancelletion Report...'

data = mysql_server('reporting', """Select concat(wadi_indexer.db,wadi_indexer.item_id)item_id,order_nr, ordered_at,exported_at,bob_item_status,vendor_code,zd.tags
                from buy_sell.wadi_indexer 
                left join
                (select item_id,tags from zendesk.zd_tickets_wadiff where date(created_at) >= curdate() - interval 45 day 
                    and tags regexp 'canc_process|bob_canceled' limit 20000)zd 
                    on zd.item_id = concat(wadi_indexer.db,wadi_indexer.item_id)
                Where date(ordered_at) >= curdate() - interval 30 day  and wadi_indexer.bob_item_status in ('exported','exportable') 
                and wadi_indexer.category_level_1 not in ( 'daily_needs','seller_accessories')
                and wadi_indexer.vendor_code >= 999
                and zd.tags is not null group by 1;""",'zendesk_tags')

if len(data) >= 1:
    print 'Sending mail...'
    fromaddr = "Harpreet Singh <harpreet.kumar>"
    toaddr = ['anshul.sharma', 'jonathan.paulson', 'megha.dani']
    tocc = ['ravi.rupak']
    #toaddr = 'harpreet.kumar'
    #tocc = 'harpreet.kumar'
    now = datetime.datetime.now()
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    msg['CC'] = ", ".join(tocc)
    msg['Subject'] = "Pending | RTS (" + now.strftime("%d %b'%Y %I:%M") + ") Cancellation" 
    body = """<html>
            <body>
            <p>Hi All,</p>
            <p>Please find attched the items marked cancelled on zendesk.</p>
            
            <p>Regards,<br>
            Proc reporting<br>
            This is an automated mail. Please contact harpreet.kumar for any query.</p>
            </body></html>"""
    
    msg.attach(MIMEText(body, 'html'))
    filename = "zendesk_tags.csv"
    attachment = open("zendesk_tags.csv", "r")

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
