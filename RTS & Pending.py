#/usr/bin/python2
from Scripts.gsheet_connect import gsheet_connect
from Scripts.Connection import mysql_server

data = mysql_server("reporting", """SELECT if(db = 'SA',sa_seller.name,ae_seller.name)vendor_name,convert(replace(replace(replace(item_name,',',''),'\r',''),'\n','') using ASCII)item_name,
concat(db,item_id)item_id,order_nr,ordered_at,
if(db = 'SA',sc_sa.fk_sales_order_item_status,sc_ae.fk_sales_order_item_status)Status,
procurement_distribution  from wadi_indexer

left join
seller_centre_ae_replica.sales_order_item sc_ae on sc_ae.src_id = wadi_indexer.item_id and wadi_indexer.db = 'AE' 

left join
seller_centre_sa_replica.sales_order_item sc_sa on sc_sa.src_id = wadi_indexer.item_id and wadi_indexer.db = 'SA'

left join
seller_centre_ae_replica.seller sa_seller on sa_seller.src_id = wadi_indexer.vendor_code

left join
seller_centre_sa_replica.seller ae_seller on ae_seller.src_id = wadi_indexer.vendor_code

left Join
erp.am_vendor_mapping am on am.vendor_name like concat('%',wadi_indexer.vendor_code,'%')

where vendor_code > 999 and (sc_sa.fk_sales_order_item_status in (1,8) or sc_ae.fk_sales_order_item_status in (1,8)) order by ordered_at;""")

data = [[str(word) for word in i] for i in data]

print data
ss = gsheet_connect("10lumM3qx89mXEGDINE6x6O8daTiwTyq_yoofIPIvOTk")
print "Google Sheet Connected!"

ss.worksheet_by_title("Data").clear()

headers = [['vendor_name', 'item_name', 'item_id', 'order_nr', 'ordered_at', 'Status', 'procurement_distribution']]
ss.worksheet_by_title("Data").update_cells("A1", headers)

if len(data) >= 1:
    ss.worksheet_by_title("Data").update_cells("A2", data)
    print "PO Pending Updated"
