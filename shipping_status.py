import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
from Scripts.Connection import mysql_server

query = """select main.*,
month(exportable_at)month,
if(shipped_at is null,0,1)is_shipped,
CASE 
 When timestampdiff(hour,exportable_at,shipped_at)/24 <=1 then '24_Hours'
 When timestampdiff(hour,exportable_at,shipped_at)/24 <=2 then '48_Hours'
 When timestampdiff(hour,exportable_at,shipped_at)/24 <=3 then 'Less_Than_72_Hours'
 When timestampdiff(hour,exportable_at,shipped_at)/24 <=5 then 'Less_Than_5_Days'
 When timestampdiff(hour,exportable_at,shipped_at)/24 >5 then 'Over_5_Days'
END as shipped_period,
CASE 
 When date(shipped_at) = date(exportable_at) then 'Same Day'
 When date(shipped_at) = date(exportable_at) + interval 1 day then 'Same Day +1'
 When date(shipped_at) = date(exportable_at) + interval 2 day then 'Same Day +2'
 When date(shipped_at) = date(exportable_at) + interval 3 day then 'Same Day +3'
 When date(shipped_at) >= date(exportable_at) + interval 4 day then '3 Day +'
END as exportable_shipped_status,-- exported-to-shipped

if(ready_to_ship is null,0,1)is_RTS,
CASE 
 When timestampdiff(hour,created_at_pending,ready_to_ship)/24 <=1 then '24_Hours'
 When timestampdiff(hour,created_at_pending,ready_to_ship)/24 <=2 then '48_Hours'
 When timestampdiff(hour,created_at_pending,ready_to_ship)/24 <=3 then 'Less_Than_72_Hours'
 When timestampdiff(hour,created_at_pending,ready_to_ship)/24 <=5 then 'Less_Than_5_Days'
 When timestampdiff(hour,created_at_pending,ready_to_ship)/24 >5 then 'Over_5_Days'
END as RTS_period,
CASE 
 When date(ready_to_ship) = date(created_at_pending) then 'Same Day'
 When date(ready_to_ship) = date(created_at_pending) + interval 1 day then 'Same Day +1'
 When date(ready_to_ship) = date(created_at_pending) + interval 2 day then 'Same Day +2'
 When date(ready_to_ship) = date(created_at_pending) + interval 3 day then 'Same Day +3'
 When date(ready_to_ship) >= date(created_at_pending) + interval 4 day then '3 Day +'
END as Pending_RTS, -- Pending-to-RTS

if(created_at_pending is null,0,1)is_created,
CASE 
 When timestampdiff(hour,exportable_at,created_at_pending)/24 <=1 then '24_Hours'
 When timestampdiff(hour,exportable_at,created_at_pending)/24 <=2 then '48_Hours'
 When timestampdiff(hour,exportable_at,created_at_pending)/24 <=3 then 'Less_Than_72_Hours'
 When timestampdiff(hour,exportable_at,created_at_pending)/24 <=5 then 'Less_Than_5_Days'
 When timestampdiff(hour,exportable_at,created_at_pending)/24 >5 then 'Over_5_Days'
END as created_period,
CASE 
 When date(created_at_pending) = date(exportable_at) then 'Same Day'
 When date(created_at_pending) = date(exportable_at) + interval 1 day then 'Same Day +1'
 When date(created_at_pending) = date(exportable_at) + interval 2 day then 'Same Day +2'
 When date(created_at_pending) = date(exportable_at) + interval 3 day then 'Same Day +3'
 When date(created_at_pending) >= date(exportable_at) + interval 4 day then '3 Day +'
END as exportable_created -- Pending-to-RTS

 
from (Select concat(wadi_indexer.db,wadi_indexer.item_id)item_id,
order_nr,
ordered_at,
bob_item_status,
wadi_indexer.sku,
bids,
replace(replace(replace(item_name,',',''),'\r',''),'\n','')item_name,
wadi_indexer.unit_price,
wadi_indexer.paid_price,
po_number,
transfer_price,
actual_cost,
stock_type,
vendor_id,
vendor_name,
shipping_location,
HAWB_number,
cancellation_reason_code,
category_level_1,
category_level_2,
category_level_3,
category_level_4,
brand,
vendor_code,
exp_date.occured_at exportable_at
,case when wadi_indexer.db = 'SA' then sc_sa.target_to_ship else sc_ae.target_to_ship end as target_to_ship
,case when wadi_indexer.db = 'SA' then sc_sa.created_at else sc_ae.created_at end as created_at_pending
,case when wadi_indexer.db = 'AE' then OH_ae.ready_for_ship_at else OH_sa.ready_for_ship_at end as ready_to_ship
,case when wadi_indexer.db = 'SA' then OH_sa.shipped_at else OH_ae.shipped_at end as shipped_at

from wadi_indexer

left join
(select db,item_id,min(occured_at +interval 4 hour)occured_at 
from status_cache 
where status = 'exportable' 
 and date(occured_at + interval 4 hour) >= date_format((curdate() - interval 1 month),"%Y-%m-01") group by 1,2)exp_date
 on exp_date.db = wadi_indexer.db and exp_date.item_id = wadi_indexer.item_id

left join
sc_live_ae.sales_order_item sc_ae on sc_ae.src_id = wadi_indexer.item_id and wadi_indexer.db = 'AE' 

left join
sc_live_sa.sales_order_item sc_sa on sc_sa.src_id = wadi_indexer.item_id and wadi_indexer.db = 'SA'

left join
	(select
    fk_sales_order_item
    ,fk_sales_order_item_status
    ,min(if(fk_sales_order_item_status = 2,created_at,null)) as shipped_at
    ,min(if(fk_sales_order_item_status = 8,created_at,null)) as ready_for_ship_at
    from  sc_live_ae.sales_order_item_status_history 
   where created_at > curdate() - interval 90 day
   group by 1
	) as OH_ae on OH_ae.fk_sales_order_item = sc_ae.id_sales_order_item

left join
	(select````````````````````
    fk_sales_order_item
    ,fk_sales_order_item_status
    ,min(if(fk_sales_order_item_status = 2,created_at,null)) as shipped_at
    ,min(if(fk_sales_order_item_status = 8,created_at,null)) as ready_for_ship_at
    from  sc_live_sa.sales_order_item_status_history 
   where created_at > curdate() - interval 90 day
   group by 1
	) as OH_sa on OH_sa.fk_sales_order_item = sc_sa.id_sales_order_item

where vendor_code > 999
and exp_date.occured_at is not null and ifnull(wadi_indexer.vendor_warehouse_country,"") not in  ('CN','HK','AF') and wadi_indexer.category_level_1 != 'daily_needs') as main;"""

data = mysql_server("reporting", query, 'MP_shipped_Orders')
now = datetime.datetime.now()

fromaddr = "Proc Team <team.procurement>"
toaddr = ['ravi.rupak']
msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['Subject'] = "MP Shipped Orders | " + now.strftime("%d %b'%Y %I:%M")

body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p>Please find attached, list of Shipped Orders for Marketplace.</p>
            <p>Regards,<br>
            Proc Reporting</p>
            </body></html> """

msg.attach(MIMEText(body, 'html'))

filename = "MP_shipped_Orders.csv"

attachment = open("MP_shipped_Orders.csv", "r")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("userid", "password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
print 'Mail Sent!!!...'
server.quit()
