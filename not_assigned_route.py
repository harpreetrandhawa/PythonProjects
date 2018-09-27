import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from Scripts.Connection import mysql_server

dropship = mysql_server('sentinel', """Select productdescription1,vendor_code,vendor_name,pickr.location,pickup_address,pickup_address from tbl_lightbox_pickr_details pickr
                        left join
                        tbl_sentinel_vendor_mapping route on route.vendorcode = pickr.vendor_code
                        where dtype='dropship' and vendor_code is not null and vendor_code not in ('MVSA001936','MVAE001496','MVSA0010 ','MVSA001049','MVAE001064','MVAE001517','V00010','V00502','V00501','MVSA001290') and (manager_name is null or manager_name = '') and 
                        route.routedetails is null 
                        group by vendor_code;""")

if len(dropship) >= 1:
    print 'Sending mail...'
    table3 = ''
    for d in dropship:
        table3 = table3+"<tr><td>"+d[0]+"</td><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"



    fromaddr = "Harpreet Singh <harpreet.kumar>"
    toaddr = ['salman.haider', 'daljeet.singh', 'khalid.abbas', 'anshul.sharma', 'rahul.chauhan', 'khalid.abbas', 'jihad.ibrahim']
    tocc = ['harpreet.kumar', 'ravi.rupak','sanyam.gupta']
    #toaddr = 'harpreet.kumar'
    #tocc = 'harpreet.kumar'
    now = datetime.datetime.now()
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    msg['CC'] = ", ".join(tocc)
    msg['Subject'] = "Route Not Assigned to Vendors | " + now.strftime("%d %b'%Y %I:%M")
    if len(dropship) >= 1:
        body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p style="color:#e46d7e">Please assign routes to the following Dropship vendors on pickr Application.</p>
            <table border = 1 cellpadding = 5 cellspacing =0><tr><th>Item_Name</th><th>Vendor_code</th><th>Vendor_name</th><th>City</th><th>Address_1</th></tr>""" + table3 + """</table>
            
            <p>Regards,<br>
            Proc reporting<br>
            This is an automated mail. Please contact harpreet.kumar for any query.</p>
            </body></html>"""
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('userid', "password")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr + tocc, text)
    print 'Mail Sent!!!...'
    server.quit()
