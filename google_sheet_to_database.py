import MySQLdb
from Scripts.Connection import mysql_server

mysql_server('sentinel', "SELECT * FROM boomerang.log_table;","log_data")

query = """LOAD DATA LOCAL INFILE 'E:\\\Proc_Reports\\\Python\\\log_data.csv' INTO TABLE my_procurement.log_table
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
