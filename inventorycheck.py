# __manish Updateinventory tools
import MySQLdb
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DBHOST =''
DBDB = ''
DBPASS = ''
DBUSER = ''


def formatqueryresult(cur):
    desc = cur.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cur.fetchall()
    ]


def executeQuerySentinel(query):
    mydb = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBDB)
    cur = mydb.cursor()
    try:
        cur.execute(query)
        dict = formatqueryresult(cur)
        mydb.commit()
        cur.close
        return dict
    except Exception, err:
        return 0
    cur.close


def updatedxbinventoryrestrict():
    executeQuerySentinel(
        "update tbl_run_details set inventory=0 where arrived_at='No' and is_cancelled=0 and is_restricted=1 and order_location in ('DXB','UAE','AE','DXBM') ")
    query = """select ee.bids,inventory,ee.qty from stock_bin_content inner join
    (select bids,count(item_id) as qty  from tbl_run_details where arrived_at='No' and is_cancelled=0 and is_restricted=1 and order_location in ('DXB','UAE','AE','DXBM') group by 1 order by ExportableDateTime asc) ee
    on ee.bids=stock_bin_content.bids where  stock_bin_content.location='DXB' and stock_bin_content.inventory !='0'"""

    data = executeQuerySentinel(query)
    for d in data:
        bids = str(d["bids"])
        inventory = str(d["inventory"])
        qty = str(d["qty"])
        if inventory != "0":
            queryinv = ""
            if inventory >= qty:
                queryinv = "update tbl_run_details set inventory='" + qty + "' where arrived_at='No' and is_cancelled=0 and is_restricted=1 and order_location in ('DXB','UAE','AE','DXBM') and bids='" + bids + "'  order by ExportableDateTime asc limit " + qty + ";"
                print queryinv
            else:
                queryinv = "update tbl_run_details set inventory='" + inventory + "' where arrived_at='No' and is_cancelled=0 and is_restricted=1 and order_location in ('DXB','UAE','AE','DXBM') and bids='" + bids + "'  order by ExportableDateTime asc limit " + inventory + ";"
                print queryinv
            executeQuerySentinel(queryinv)
        else:
            print inventory
            print "=================== Zero==============="
    print "Done DXB"


def updateksainventoryrestrict():
    executeQuerySentinel(
        "update tbl_run_details set inventory=0 where arrived_at='No' and is_cancelled=0 and is_restricted=1 and order_location in ('KSA','SA','KSAM') ")
    query = """select ee.bids,inventory,ee.qty from stock_bin_content inner join
(select bids,count(item_id) as qty from tbl_run_details where arrived_at='No' and is_cancelled=0 and is_restricted=1 and order_location in ('KSA','SA','KSAM') group by 1 order by ExportableDateTime asc) ee
on ee.bids=stock_bin_content.bids where  stock_bin_content.location='KSA' and stock_bin_content.inventory !='0'"""
    data = executeQuerySentinel(query)
    for d in data:
        bids = str(d["bids"])
        inventory = str(d["inventory"])
        qty = str(d["qty"])
        print inventory
        print qty
        if inventory != "0":
            queryinv = ""
            if inventory >= qty:
                queryinv = "update tbl_run_details set inventory='" + qty + "' where arrived_at='No' and is_cancelled=0 and is_restricted=1 and order_location in ('KSA','KSAM','SA') and bids='" + bids + "'  order by ExportableDateTime asc limit " + qty + ";"
                print queryinv
            else:
                queryinv = "update tbl_run_details set inventory='" + inventory + "' where arrived_at='No' and is_cancelled=0 and is_restricted=1 and order_location in ('KSA','KSAM','SA') and bids='" + bids + "'  order by ExportableDateTime asc limit " + inventory + ";"
                print queryinv
            executeQuerySentinel(queryinv)
        else:
            print inventory
            print "=================== Zero==============="
    print "Done KSA"


def updateksainventorynonrestrict():
    print "call"
    executeQuerySentinel(
        "update tbl_run_details set inventory=0 where arrived_at='No' and is_cancelled=0 and is_restricted=0 ")
    query = """select sbc.bids,sbc.location,sbc.inventory,ee.qty,ee.dxbqty,ee.ksaqty,(select sum(inventory) from stock_bin_content where bids=sbc.bids) as total from stock_bin_content sbc inner join 
(select bids,count(item_id) as qty,sum(if(order_location='DXB'or order_location='UAE' or order_location='AE' or order_location='DXBM',1,0)) as dxbqty,
sum(if(order_location='KSA'or order_location='SA'or order_location='KSAM' ,1,0)) as ksaqty from tbl_run_details where arrived_at='No' and is_cancelled=0 and is_restricted=0  group by 1 ) ee
on ee.bids=sbc.bids where sbc.inventory !='0' order by sbc.bids;"""
    print query
    data = executeQuerySentinel(query)
    updatedarr=[]
    for d in data:
        bids=str(d["bids"])
        location=str(d["location"])
        inventory=str(d["inventory"])
        qty=str(d["qty"])
        dxbqty=str(d["dxbqty"])
        ksaqty=str(d["ksaqty"])
        totalinventory=str(d["total"])
        if inventory !="0":
            if inventory >=ksaqty:
                print "in if"
                queryinv=""
                if location == 'DXB':
                    pass
                    # print dxbqty + " DXBQTY"
                    # print ksaqty + " KSAQTY"
                    # print qty +" QTY"
                    # print inventory +" Inventory"
                    # print  totalinventory+ " Total"
                    # print  location+ " Location"
                else:

                    print qty +" QTY"
                    print ksaqty + " KSAQTY"
                    print dxbqty + " DXBQTY"
                    print inventory + " Inventory"
                    print totalinventory + " Total"
                    print location + " Location"
                    queryinv = "update tbl_run_details set inventory='" + qty + "' where arrived_at='No' and is_cancelled=0 and is_restricted=0 and order_location in ('KSA','SA','KSAM') and bids='" + bids + "'  order by ExportableDateTime asc limit " + qty + ";"
                    print queryinv
                    #updatedarr.append([bids,ksaqty,inventory,totalinventory,location])
                executeQuerySentinel(queryinv)


            else:
                print "Out if"
                if location == 'DXB':
                    pass
                    # print dxbqty + " DXBQTY"
                    # print ksaqty + " KSAQTY"
                    # print qty +" QTY"
                    # print inventory +" Inventory"
                    # print  totalinventory+ " Total"
                    # print  location+ " Location"
                else:
                    pass
                    # print qty + " QTY"
                    # print ksaqty + " KSAQTY"
                    # print dxbqty + " DXBQTY"
                    # print inventory + " Inventory"
                    # print totalinventory + " Total"
                    # print location + " Location"
            print updatedarr







def main():
    try:
        # **************REStrict**************************************
        updateksainventoryrestrict()
        updatedxbinventoryrestrict()
        # **************Non Restrict ***************************************
        #updateksainventorynonrestrict()

        urllib2.urlopen("")
        print 'Success'
    except Exception, err:
        print err


if __name__ == "__main__":
    main()
