#/usr/bin/python2
from Scripts.gsheet_connect import gsheet_connect
from Scripts.Connection import mysql_server

###################################################################
print 'Updating GoogleSheet Dashboard...'

ss = gsheet_connect("sheet_id")
print "Google Sheet Connected!"

def dashboard():
    data = mysql_server("reporting", "query")

    data = [[str(word) for word in i] for i in data]
    if len(data) >= 1:
        ss.worksheet_by_title("Data").update_cells("B5", data)
        print "DashBoard Updated!"

########################################################################################

def Charts_updation():
    data = mysql_server("reporting", "query")

    data = [[str(word) for word in i] for i in data]
    if len(data) >= 1:
        ss.worksheet_by_title("Data").update_cells("B5", data)
        print "DashBoard Updated!"




def main():
    try:
        dashboard()
    except Exception, Err:
        print Err


if __name__ == "__main__":
    main()
