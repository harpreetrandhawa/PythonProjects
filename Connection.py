#/usr/bin/python2
import csv
import pymysql
import pygsheets

#************************MySQL Server*********************#

def mysql_server(server, query, save_as=None):
    """Connect MySQL Server, Need server_name,query or query path, file's name to save_result which is Optional"""
    try:
        filepath = 'Path' + server + '.csv'

        print 'Checking Connections...'
        credentials = [line for line in open(filepath, 'r')]
        dbUser = credentials[0].replace('\n', '')
        dbPass = credentials[1].replace('\n', '')
        dbServer = credentials[2].replace('\n', '')
        port = int(credentials[3].replace('\n', ''))
        dbSchema = credentials[4].replace('\n', '')

        if query.find('\\') != -1:
            dbQuery = open(query, 'r').read()
        else:
            dbQuery = query
        conn = pymysql.connect(host=dbServer, port=port, user=dbUser, passwd=dbPass, db=dbSchema)
        print 'Connected Successfully!!!'
        cur = conn.cursor()
        cur.execute(dbQuery)
        result = cur.fetchall()
        if save_as != None:
            f = csv.writer(open(save_as +".csv", "wb"))
            f.writerow([i[0] for i in cur.description])
            for row in result:
                f.writerow(row)
        print 'Reading Data...'
        return result
    except Exception as e:
        print str(e)
        return False

#************************MySQL Server*********************#

def gsheet_connect(gsheet_key):
    """Connect to Google Spreadsheet using gsheet_id"""
    gc = pygsheets.authorize(service_file='path.json', no_cache=True)
    ss = gc.open_by_key(gsheet_key)
    print "Google Sheet Connected!"
    return ss
    
