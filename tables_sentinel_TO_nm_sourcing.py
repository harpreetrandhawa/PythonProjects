import MySQLdb
from Scripts.Connection import mysql_server

def log_table():
    mysql_server('sentinel', "SELECT * FROM boomerang.log_table where date(timestamp) >= curdate() - interval 1 day ;", "log_data")
    #truncate_query = "truncate Returns.log_table"

    query = """LOAD DATA LOCAL INFILE 'E:\\\Proc_Reports\\\Python\\\log_data.csv' REPLACE INTO TABLE Returns.log_table
    FIELDS TERMINATED BY ',' 
    ENCLOSED BY '"' 
    LINES TERMINATED BY '\\r\\n'
    IGNORE 1 LINES"""


    filepath = 'E:\\Proc_Reports\\credentials\\nm_sourcing.csv'

    print 'Checking Connections...'
    credentials = [line for line in open(filepath, 'r')]
    dbUser = credentials[0].replace('\n', '')
    dbPass = credentials[1].replace('\n', '')
    dbServer = credentials[2].replace('\n', '')
    port = int(credentials[3].replace('\n', ''))
    dbSchema = credentials[4].replace('\n', '')

    conn = MySQLdb.connect(host=dbServer, port=port, user=dbUser, passwd=dbPass, db=dbSchema)
    print 'Connected Successfully!!!'
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

def return_sales_order_item():
    mysql_server('sentinel', """SELECT id,HAWB_number,return_awb,item_id,erp_id,order_nr,
bob_item_status,return_sales_order_itemcol,shipped_at,RTO_initiated_date,
return_delivered,vendor_id,ascii(vendor_name),ascii(vendor_code),consignment_type,short_code,ascii(vendor_address),vendor_contact,
vendor_email,route,unit_price,delivered_at,return_type,ascii(item_name),po_number,po_created_at,ordered_at,is_active,
flg,created_date,modified_date,last_modified_date,city,location,item_status,step,carrier_id,carrier_name,
scanned_at,pdf_link FROM boomerang.return_sales_order_item where date(last_modified_date) >= curdate() - interval 1 day""", "Return_sales_order_item")

    query = """LOAD DATA LOCAL INFILE 'E:\\\Proc_Reports\\\Python\\\Return_sales_order_item.csv' REPLACE INTO TABLE Returns.returns_table
    FIELDS TERMINATED BY ',' 
    ENCLOSED BY '"' 
    LINES TERMINATED BY '\\r\\n'
    IGNORE 1 LINES"""


    filepath = 'E:\\Proc_Reports\\credentials\\nm_sourcing_gopal.csv'

    print 'Checking Connections...'
    credentials = [line for line in open(filepath, 'r')]
    dbUser = credentials[0].replace('\n', '')
    dbPass = credentials[1].replace('\n', '')
    dbServer = credentials[2].replace('\n', '')
    port = int(credentials[3].replace('\n', ''))
    dbSchema = credentials[4].replace('\n', '')

    conn = MySQLdb.connect(host=dbServer, port=port, user=dbUser, passwd=dbPass, db=dbSchema)
    print 'Connected Successfully!!!'
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()


def main():
    try:
        log_table()
        print "log_table Updated!!!"
        return_sales_order_item()
        print "return_sales_order_item Updated!!!"
    except Exception, Err:
        print Err

if __name__ == "__main__":
    main()
