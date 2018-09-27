import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from Scripts.Connection import mysql_server

data = mysql_server('sentinel', 'C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\not_assigned_vendors.sql')
Data1 = mysql_server('sentinel', 'C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\not_assigned_Mplace.sql')
dropship = mysql_server('sentinel', """select productdescription1,vendor_code,vendor_name,location,pickup_address,pickup_address 
                                        from tbl_lightbox_pickr_details 
                                        where dtype = 'dropship' and (manager_name = '' or manager_name is null) 
                                        and  vendor_code not in ('MVAE001496','MVSA0010 ','MVSA001049','MVAE001064','MVAE001517','V00010','MVSA001290')  group by 2;""")
print dropship
if len(data) >= 1 or len(Data1) >= 1 or len(dropship) >= 1:
    print 'Sending mail...'
    table = ''
    for d in data:
        table = table+"<tr><td>"+d[0]+"</td><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td></tr>"
    table1 = ''
    for d in Data1:
        table1 = table1+"<tr><td>"+d[0]+"</td><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td></tr>"                                               
    table3 = ''
    for d in dropship:
        table3 = table3+"<tr><td>"+d[0]+"</td><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td><td>"+str(d[5])+"</td></tr>"



    fromaddr = "Procurement Reporting <team.procurement>"
    toaddr = 'procurement,mubina.badat,amr.hanafi,sankeerth.nadipalli,ritesh.pande,adegboye.bukola,shobhit.agrawal,ragini.singh,aleem.muneer'
    tocc = 'harpreet.kumar,shubham.trivedi,ravi.rupak,sanyam.gupta'
    #toaddr = 'ravi.rupak,harpreet.kumar'
    #tocc = '' #'harpreet.kumar,shubham.trivedi'
    now = datetime.datetime.now()
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['CC'] = tocc
    msg['Subject'] = "Not Assigned Vendors | " + now.strftime("%d %b'%Y %I:%M")
    if len(Data1) >= 1 or len(dropship) >= 1:
        body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p style="color:#e46d7e">Please assign the following Dropship vendors on LightBox under pickr Application.</p>
            <table border = 1 cellpadding = 5 cellspacing =0><tr><th>Item_Name</th><th>Vendor_code</th><th>Vendor_name</th><th>City</th><th>Address_1</th><th>Address_2</th></tr>""" + table3 + """</table>
            <p>Please assign the following MarketPlace vendors on LightBox under pickr Application.</p>
            <table border = 1 cellpadding = 5 cellspacing =0><tr><th>Item_Name</th><th>Vendor_code</th><th>Vendor_name</th></tr>""" + table1 + """</table>
            <p>Please assign the following vendors on Sentinel.</p>
            <table border = 1 cellpadding = 5 cellspacing =0><tr><th>Item_Name</th><th>Category</th><th>Vendor_code</th><th>Vendor_name</th></tr>""" + table + """</table>
            <p>Regards,<br>
            Proc reporting</p>
            </body></html> """
    else:
        body = """<html>
            <body>
            <p>Hi Team,</p>
            <p>Please assign the following vendors on LightBox under pickr Application.</p>
            <table border = 1 cellpadding = 5 cellspacing =0><tr><th>Item_Name</th><th>Category</th><th>Vendor_code</th><th>Vendor_name</th></tr>""" + table + """</table>
            <p>Regards,<br>
            Proc reporting</p>
            </body></html>"""
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('userid', "password")
    text = msg.as_string()
    server.sendmail(fromaddr, [toaddr, tocc], text)
    print 'Mail Sent!!!...'
    server.quit()
