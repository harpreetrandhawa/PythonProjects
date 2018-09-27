#/usr/bin/python2
import smtplib
from email.mime import multipart as MIMEMultipart
from email.mime.text import MIMEText
import datetime
from Scripts.Connection import mysql_server

Query = """select Itemid,skucode,po,productdescription,ifnull(if(recd_qty!=0,'Qty Recevied',ps.status),'-') as status,driver,
paymentterms,country,lvu.vendor_id,vendor_name,modified_date,ifnull(driver_status,'-') as driverstatus from
tbl_lightbox_vendor_update lvu
left join
tbl_sentinel_vendor_mapping svm
on svm.vendorcode = lvu.vendor_id
left join
tbl_pickr_assign_status ps
on ps.id=lvu.driver_action
where date(lvu.created_date)=curdate() and is_arrivel='No' 
and vendor_id in (select vendorcode from tbl_sentinel_vendor_mapping where routedetails='Route 2')"""

data = mysql_server('sentinel',Query)
print data
