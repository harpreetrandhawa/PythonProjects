#/usr/bin/python2
import MySQLdb
from Scripts.Connection import mysql_server

data = mysql_server('pricing','select * from wadi_retail.higher_stocks where date(end_date) >= curdate()', 'data')
mysql_server('nm_sourcing','truncate')



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
