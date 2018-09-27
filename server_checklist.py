#/usr/bin/python2
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import MySQLdb


def formatqueryresult(cur):
    desc = cur.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cur.fetchall()
    ]

def reporting(query):
    mydb = MySQLdb.connect(host='', user='', passwd='', db='')
    cur = mydb.cursor()
    try:
        cur.execute(query)
        dict = cur.fetchall()
        dict = str(dict[0][0])
        mydb.commit()
        cur.close
        return dict
    except Exception, err:
        return 0
    cur.close

def nm_sourcing(query):
    mydb = MySQLdb.connect(host='', user='', passwd='', port=3316, db='')
    cur = mydb.cursor()
    try:
        cur.execute(query)
        dict = cur.fetchall()
        dict = str(dict[0][0])
        mydb.commit()
        cur.close
        return dict
    except Exception, err:
        return 0
    cur.close




def not_running(table):
    fromaddr = "Procurement Reporting <team.procurement>"
    toaddr = ['harpreet.kumar', 'manish.kumar', 'shubham.trivedi']
    msg = MIMEMultipart()
    msg['Subject'] = 'Server Checks: ' + table + ' is Down.'
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    content = '<html><body><p>Team, '+table+' is Down</p></body></html>'
    msg.attach(MIMEText(content, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('', "")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print 'Mail Sent'

def custom_table_check():
    """Checking sales_order_item_custom table on nm_sourcing Server."""
    table = "'sales_order_item_custom_new'"
    r_item = reporting("select item_id from wadi_indexer where bob_item_status in ('exported','exportable') order by 1 desc limit 1;")
    n_item = nm_sourcing("select id_sales_order_item from sales_order_item_custom_new where status in ('exported','exportable') order by 1 desc limit 1;")
    if n_item < r_item:
        not_running(table)
    else:
        print "nm_sourcing.sales_order_item_custom_new is UP."

def replica_sales_erp_check():
    table = "'replica_sales_order_item_erp'"
    updated_at = nm_sourcing("select max(erp_updated_at + interval 4 hour) from replica_sales_order_item_erp;")
    updated_at = datetime.datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')
    if updated_at < (datetime.datetime.now() - datetime.timedelta(hours= 1, minutes= 50)):
        not_running(table)
    else:
        print "nm_sourcing.replica_sales_order_item_erp is UP."

def vendor_ranking_check():
    table = "'nm_sourcing.vendor_ranking'"
    r_count = reporting('Select count(1) from wadi_retail.vendor_ranking;')
    nm_count = nm_sourcing("select count(1) from vendor_ranking;")
    if int(r_count) > int(nm_count):
        not_running(table)
    else:
        print "nm_sourcing.vendor_ranking is UP."

def vendor_mapping_check():
    table = "'nm_sourcing.replica_am_vendor_mapping'"
    r_count = reporting('Select count(1) from erp.am_vendor_mapping;')
    nm_count = nm_sourcing("select count(1) from replica_am_vendor_mapping;")
    if int(r_count) > int(nm_count):
        not_running(table)
    else:
        print "nm_sourcing.replica_am_vendor_mapping is UP."


def main():
    
    try:
        custom_table_check()
        replica_sales_erp_check()
        vendor_ranking_check()
        vendor_mapping_check()
    except Exception, Err:
        print Err


if __name__ == "__main__":
    main()
