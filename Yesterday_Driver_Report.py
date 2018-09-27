import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from Scripts.Connection import mysql_server

Data1 = mysql_server('sentinel', """select replace(replace(driver,'\n',''),'\r','') from tbl_pickr_driver_dropship_updates  group by driver;""")
#dropship = mysql_server('sentinel', "select item_discreption,vendorCode,vendor_name,fk_city,fk_address1,fk_address2 from tbl_lightbox_pickr_dropship where vendorCode not in ('MVAE001496','MVSA0010 ','MVSA001049') and manager_name = '' or manager_name is null group by 2;")

table = ""
tableh=""
table =""
td1=""
td2=""
td3=""
for d in Data1:
    driver_name = d[0]
    tableh=tableh+"<th>"+driver_name+"</th>"
    order_count = mysql_server('sentinel',"""select '"""+driver_name+ """' driver ,status,count(id)qty,(select loc from tbl_senitel_user_master where first_name='"""+driver_name+ """') as loc   from (select id,recd_qty,fk_city,Attempt, if(Attempt=0,'Not Attempt',if(recd_qty=1,'Picked','Not Picked')) as status from tbl_lightbox_pickr_dropship  where date(modified_date) = curdate()- interval 1 day and vendorCode in (
    select vendorcode from tbl_sentinel_vendor_mapping where routedetails in (
    select route from tbl_picker_driver_run_details where did in (select uid from tbl_senitel_user_master where first_name='"""+driver_name+ """'))) )t group by status""" )

    sum=0
    at=[]
    if len(order_count)>0:
        for i in range(3):
            driverstatus=""
            drivercount=""
            driverloc=""
            sum=sum+1
            print sum
            try:
                driverstatus=str(order_count[i][1])
                drivercount=str(order_count[i][2])
                driverloc=str(order_count[i][3])
                at.append(driverstatus)
            except Exception,err:
                if "Not Attempt" not in at:
                    td1=td1+"<td></td>"
                elif "Picked"  not in at:
                    td2=td2+"<td></td>"
                else:
                    td3=td3+"<td></td>"
                pass
            print driverstatus
        # for d1 in order_count:
        #     driverstatus=str(d1[1])
        #     drivercount=str(d1[2])
        #     driverloc=d1[3]
        
            if driverstatus=='Not Attempt':
                td1=td1+"<td>"+drivercount+"</td>"
            elif driverstatus=='Picked':
                td2=td2+"<td>"+drivercount+"</td>"
            elif driverstatus=='Not Picked':
                td3=td3+"<td>"+drivercount+"</td>"
    else:
        print "no data"           
       
        
print td1
print td2
print td3
if td1!="":
    table = table +"<tr><td>Not Attempt</td>"+ td1+"</tr><tr><td>Picked</td>"+td2+"</tr><tr><td>Not Picked</td>"+td3+"</tr>"
    print table

        

    print tableh



    fromaddr = "Procurement Reporting <team.procurement>"
    #toaddr = 'procurement,mubina.badat,sankeerth.nadipalli,ritesh.pande,adegboye.bukola,shobhit.agrawal,ragini.singh'
    #tocc = 'harpreet.kumar,shubham.trivedi'
    toaddr = ['harpreet.kumar', 'manish.kumar']
    tocc = ['harpreet.kumar']
    now = datetime.datetime.now()
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    msg['CC'] = ", ".join(tocc)
    msg['Subject'] = "Driver Bifurcation | " + now.strftime("%d %b'%Y %I:%M")
    if len(Data1) >= 1:
        body = """ <html>
            <body>
            <p>Hi Team,</p>
            <p>Please find below bifurcation for Items picked by drivers.</p>
            <table border = 1 cellpadding = 5 cellspacing =0><tr><th>Action</th>"""+tableh+"""</tr>""" + table + """</table>
            <p>Regards,<br>
            Proc reporting</p>
            </body></html> """
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('userid', "password")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr+tocc, text)
    print 'Mail Sent!!!...'
    server.quit()
else:
    print "Not found"
