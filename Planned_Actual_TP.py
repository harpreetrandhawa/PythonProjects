import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from Scripts.Connection import mysql_server
import datetime

data = mysql_server('sentinel', 'C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\Planned_Actual_TP_DXB.sql', 'Planned_vs_Actual_TP')
data1 = mysql_server('sentinel', 'C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\Planned_Actual_TP_Data.sql', 'Planned_vs_Actual_TP_Data')
data2 = mysql_server('sentinel', 'C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\Planned_Actual_TP_KSA.sql', 'Planned_vs_Actual_TP')
MTD = mysql_server('sentinel', 'C:\\Users\\randh\\Google Drive\\Proc Reports\\SQL\\Planned_Actual_TP_MTD.sql', 'Planned_vs_Actual_MTD')

if len(data1) >= 1:
    print('Sending mail...')
    mtd = str(MTD[0][0])

    assign_tp = sum(row[1] for row in data)
    arrive_tp = sum(row[2] for row in data)

    assign_tp = assign_tp + sum(row[1] for row in data2)
    arrive_tp = arrive_tp + sum(row[2] for row in data2)
    percentage = round((arrive_tp-assign_tp)/assign_tp*100, 2)

    table=''
    for d in data:
        dhtml=""
        if str(d[3]) == '0.00%':
            dhtml="<span >"+str(d[3])+"</span>"
        elif '-' in str(d[3]):
                dhtml="<span style='color:green'><b>"+str(d[3])+"</b></span>"
        elif str(d[3]) !='0.00%' and str(d[3]) not in '-':
                dhtml="<span style='color:red'><b>"+str(d[3])+"</b></span>" 
        table=table+"<tr><td>"+str(d[0])+"</td><td style='text-align: center;'>"+str(d[1])+"</td><td style='text-align: center;'>"+str(d[2])+"</td><td style='text-align: center;'>"+dhtml+"</td></tr>"

    table1 =''
    for r in data2:
        dhtml1=""
        if str(r[3]) == '0.00%':
            dhtml1="<span >"+str(r[3])+"</span>"
        elif '-' in str(r[3]):
            dhtml1="<span style='color:green'><b>"+str(r[3])+"</b></span>"
        elif str(r[3]) !='0.00%' and str(r[3]) not in '-':
            dhtml1="<span style='color:red'><b>"+str(r[3])+"</b></span>" 
        table1=table1+"<tr><td>"+str(r[0])+"</td><td style='text-align: center;'>"+str(r[1])+"</td><td style='text-align: center;'>"+str(r[2])+"</td><td style='text-align: center;'>"+dhtml1+"</td></tr>"


    fromaddr = "Procurement Reporting <team.procurement>"
    toaddr = ['sanyam.gupta']
    tocc = ['harpreet.kumar']
    now = datetime.datetime.now()
    msg = MIMEMultipart()
         
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    msg['CC'] = ", ".join(tocc)
    msg['Subject'] = "Planned v/s Actual TP: Yesterday: " + str(percentage) + "% | MTD: " + mtd + "% (" + now.strftime("%d %b'%Y %I:%M") +")"

    body = """ <html>
                <body>
                <p>Hi Team,</p>
                <p>Please find below details regarding planned v/s actual tp (Sheet attached for reference):</p>
                <p>Dubai (Basis of items arrived in DXB W/H yesterday):</p>
                <table border = 1 cellpadding = 5 cellspacing =0><tr style = "background-color: #afd4ea"><th>Category</th><th>Planned</th><th>Actual</th><th>% Diff.</th></tr>""" + table + """</table>           
                <p>Saudi (Basis of items arrived in KSA W/H yesterday):</p>
                <table border = 1 cellpadding = 5 cellspacing =0><tr style = "background-color: #afd4ea"><th>Category</th><th>Planned</th><th>Actual</th><th>% Diff.</th></tr>""" + table1 + """</table>           
                <p>Regards,<br>
                Proc reporting</p>
                </body></html> """
    msg.attach(MIMEText(body, 'html'))

    filename = "Planned_vs_Actual_TP_Data.csv"
    attachment = open("Planned_vs_Actual_TP_Data.csv", "r")
        
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
    msg.attach(part)
         
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('userid', "password")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr + tocc, text)
    print('Mail Sent!!!...')
    server.quit()
