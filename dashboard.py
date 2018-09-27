#/usr/bin/python2
from Scripts.gsheet_connect import gsheet_connect
from Scripts.Connection import mysql_server

data = mysql_server("reporting", "query")

data = [[str(word) for word in i] for i in data]
#data = [list(i) for i in data]

ss = gsheet_connect("sheet_id")
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

def main():
    try:
        ksa_arrival_report()
        print "ksa_arrival_report Sent!!!"
        dxb_arrival_report()
        print "dxb_arrival_report Sent!!!"
    except Exception, Err:
        print Err

if __name__ == "__main__":
    main()
    
