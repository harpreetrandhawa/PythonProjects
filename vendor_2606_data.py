#/usr/bin/python2
from Scripts.gsheet_connect import gsheet_connect
from Scripts.Connection import mysql_server

data = mysql_server("reporting", """select concat(db,item_id)item_id,order_nr,bob_item_status,seller_sku,
convert(replace(replace(replace(item_name,',',''),'\r',''),'\n','') using ASCII)item_name,
cast(ifnull(seller_special_price_sa,seller_price_sa) as char)price from wadi_indexer 
where po_created_at is null and erp_canceled_at is null 
and bob_item_status in ('exported','exportable') and vendor_code = '2606';""")

data1 = mysql_server("reporting", """select concat(db,item_id)item_id,order_nr,bob_item_status,seller_sku,
convert(replace(replace(replace(item_name,',',''),'\r',''),'\n','') using ASCII)item_name,
cast(ifnull(seller_special_price_sa,seller_price_sa) as char)price from wadi_indexer 
where po_created_at is not null and erp_canceled_at is null and bob_item_status in ('exported','exportable') and vendor_code = '2606';""")

can_data = mysql_server("reporting", """select concat(db,item_id)item_id,order_nr,bob_item_status,seller_sku,
convert(replace(replace(replace(item_name,',',''),'\r',''),'\n','') using ASCII)item_name,
cast(ifnull(seller_special_price_sa,seller_price_sa) as char)price from wadi_indexer 
where erp_canceled_at is not null and vendor_code = '2606';""")

ship_data = mysql_server("reporting", """select concat(db,item_id)item_id,order_nr,bob_item_status,seller_sku,
convert(replace(replace(replace(item_name,',',''),'\r',''),'\n','') using ASCII)item_name,
cast(ifnull(seller_special_price_sa,seller_price_sa) as char)price from wadi_indexer 
where shipped_at is not null and vendor_code = '2606';""")

delivered_data = mysql_server("reporting", """select concat(db,item_id)item_id,order_nr,bob_item_status,seller_sku,
convert(replace(replace(replace(item_name,',',''),'\r',''),'\n','') using ASCII)item_name,
cast(ifnull(seller_special_price_sa,seller_price_sa) as char)price from wadi_indexer 
where bob_item_status in ('delivered','delivered_and_paid') and vendor_code = '2606';""")

data = [[str(word) for word in i] for i in data]
#data = [list(i) for i in data]
data1 = [list(i) for i in data1]
can_data = [list(i) for i in can_data]
ship_data = [list(i) for i in ship_data]
delivered_data = [list(i) for i in delivered_data]

ss = gsheet_connect("1K3fXnOVFt7H40YeamzmJ67T6vXbFB4P9w_O_Mo8OrrM")
print "Google Sheet Connected!"

ss.worksheet_by_title("PO Pending").clear()
ss.worksheet_by_title("PO Created").clear()
ss.worksheet_by_title("Cancelled").clear()
ss.worksheet_by_title("Shipped").clear()
ss.worksheet_by_title("Delivered").clear()

headers = [['item_id', 'order_nr', 'bob_item_status', 'seller_sku', 'item_name', 'price']]
ss.worksheet_by_title("PO Pending").update_cells("A1", headers)
ss.worksheet_by_title("PO Created").update_cells("A1", headers)
ss.worksheet_by_title("Cancelled").update_cells("A1", headers)
ss.worksheet_by_title("Shipped").update_cells("A1", headers)
ss.worksheet_by_title("Delivered").update_cells("A1", headers)

if len(data) >= 1:
    ss.worksheet_by_title("PO Pending").update_cells("A2", data)
    print "PO Pending Updated"
if len(data1) >= 1:
    ss.worksheet_by_title("PO Created").update_cells("A2", data1)
    print "PO Created Updated"
if len(can_data) >= 1:
    ss.worksheet_by_title("Cancelled").update_cells("A2", can_data)
    print "Cancelled Updated"
if len(ship_data) >= 1:
    ss.worksheet_by_title("Shipped").update_cells("A2", ship_data)
    print "Shipped Updated"
if len(delivered_data) >= 1:
    ss.worksheet_by_title("Delivered").update_cells("A2", delivered_data)
    print "Delivered Updated"
    
