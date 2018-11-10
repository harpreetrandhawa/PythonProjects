#/usr/bin/python2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
from Scripts.Connection import mysql_server

#***********************FOR KSA Reports*********************************
def ksa_arrival_report():
    indv = mysql_server('nm_sourcing', 'Path')
    indv_mtd = mysql_server('nm_sourcing', 'Path')
    MTD = mysql_server('nm_sourcing', 'path')
    
    mysql_server('nm_sourcing', "query", 'KSA_Arrival_yesterday')

    if len(indv) >= 1:
        print("Sending Mail")
        htmlrow1 = ""
        htmlrow2 = ""
        htmlrow3 = ""
        htmlrow4 = ""
        htmlrow5 = ""
        htmlrow6 = ""
        htmlrow7 = ""
        htmlrow8 = ""
        for d in indv:
            htmlrow1 = htmlrow1 + "<td>" + str(d[0]) + "</td>"
            htmlrow2 = htmlrow2 + "<td>" + str(d[1]) + "</td>"
            htmlrow3 = htmlrow3 + "<td>" + str(d[2]) + "</td>"
            htmlrow4 = htmlrow4 + "<td>" + str(d[3]) + "</td>"
            htmlrow5 = htmlrow5 + "<td>" + str(d[4]) + "</td>"
            htmlrow6 = htmlrow6 + "<td>" + str(d[5]) + "</td>"
            htmlrow7 = htmlrow7 + "<td>" + str(d[6]) + "</td>"
            htmlrow8 = htmlrow8 + "<td>" + str(d[7]) + "</td>"
        table_invd = "<tr style = 'background-color: #afd4ea'><td></td>"+htmlrow1+"</tr><tr><td>12 hours</td>"+htmlrow2+"</tr><tr><td>24 hours</td>"+htmlrow3+"</tr><tr><td>48 Hours</td>"+htmlrow4+"</tr><tr><td>72 Hours</td>"+htmlrow5+"</tr><tr><td>Above 72 Hours</td>"+htmlrow6+"</tr><tr><td left; colspan='6'></td></tr><tr><td>Arrived Items</td>"+htmlrow8+"</tr><tr><td>Arrival TAT (Days)</td>"+htmlrow7+"</tr>"
        htmlrow1 = ""
        htmlrow2 = ""
        htmlrow3 = ""
        htmlrow4 = ""
        htmlrow5 = ""
        htmlrow6 = ""
        htmlrow7 = ""
        htmlrow8 = ""
        for d in indv_mtd:
            htmlrow1 = htmlrow1+"<td>" + str(d[0])+"</td>"
            htmlrow2 = htmlrow2+"<td>" + str(d[1])+"</td>"
            htmlrow3 = htmlrow3+"<td>" + str(d[2])+ "</td>"
            htmlrow4 = htmlrow4+"<td>" + str(d[3]) + "</td>"
            htmlrow5 = htmlrow5+"<td>" + str(d[4]) + "</td>"
            htmlrow6 = htmlrow6+"<td>" + str(d[5]) + "</td>"
            htmlrow7 = htmlrow7+"<td>" + str(d[6]) + "</td>"
            htmlrow8 = htmlrow8+"<td>" + str(d[7]) + "</td>"
        table_invd_mtd = "<tr style = 'background-color: #afd4ea' ><td></td>"+htmlrow1+"</tr><tr><td>12 hours</td>"+htmlrow2+"</tr><tr><td>24 hours</td>"+htmlrow3+"</tr><tr><td>48 Hours</td>"+htmlrow4+"</tr><tr><td>72 Hours</td>"+htmlrow5+"</tr><tr><td>Above 72 Hours</td>"+htmlrow6+"</tr><tr><td left; colspan='6'></td></tr><tr><td>Arrived Items</td>"+htmlrow8+"</tr><tr><td>Arrival TAT (Days)</td>"+htmlrow7+"</tr>"
        fromaddr = "Procurement Reporting <team.procurement>"
        toaddr = []
        tocc = []
        #toaddr = ['harpreet.kumar']
        #tocc = ['harpreet.kumar']
        now = datetime.datetime.now()
        yest = now - datetime.timedelta(1)
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ", ".join(toaddr)
        msg['CC'] = ", ".join(tocc)
        msg['Subject'] = "Saudi Procurement " + yest.strftime("%d-%b") + " | MTD in 48 hrs : "+ MTD[0][2]
        body = """ <html>
                    <body>
                    <p>Hi Team,</p>
                    <p>Please find below details regarding this month performance:</p>

                    <p><b><u>Overall MTD:</u></b></p>
                    <table border = 1 cellpadding = 5 cellspacing =0>
                    <tr style = "background-color: #afd4ea">
                    <th text-align: left; colspan='2' >% Arrival(JIT)</th>
                    <th text-align: center>Targets</th>
                    </tr><tr><td>12 Hours</td><td>"""+ MTD[0][0]+"""</td><td>30%</td></tr>
                    <tr><td>24 Hours</td><td>"""+ MTD[0][1]+"""</td><td>50%</td></tr>
                    <tr><td>48 Hours</td><td>"""+ MTD[0][2]+"""</td><td>70%</td></tr>
                    <tr><td>72 Hours</td><td>"""+ MTD[0][3]+"""</td><td>85%</td></tr>
                    <tr><td>Above 72 Hours</td><td>"""+ MTD[0][4]+"""</td><td>85% +</td></tr>
                    <tr><td colspan='3'></td></tr>
                    <tr><td>Arrived Items</td><td style = "text-align: center" colspan="2">"""+ str(MTD[0][6])+"""</td></tr>
                    <tr><td>Arrival TAT (Days) </td><td style = "text-align: center" colspan="2">"""+ str(MTD[0][5])+"""</td></tr>
                    </table>
                    
                    <p><b><u>Individual MTD:</u></b></p>
                    <table border = 1 cellpadding = 5 cellspacing =0>
                    """+ table_invd_mtd + """</table>

                    <p><b><u>Individual Yesterday:</u></b></p>
                    <table border = 1 cellpadding = 5 cellspacing =0>
                    """+ table_invd +"""</table>
                    
                    <p>Regards,<br>
                    Proc reporting</p>
                    </body></html> """
        msg.attach(MIMEText(body, 'html'))

        filename = "KSA_Arrival_yesterday.csv"
        attachment = open("KSA_Arrival_yesterday.csv", "r")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('user_id', "password")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr + tocc, text)
        print("Mail Sent...")
        server.quit()

#************************DXB Arrival Report*********************#
def dxb_arrival_report():
    indv = mysql_server('nm_sourcing', 'path')
    indv_mtd = mysql_server('nm_sourcing', 'path')
    MTD = mysql_server('nm_sourcing', 'path')

    mysql_server('nm_sourcing', "query", 'DXB_Arrival_yesterday')

    if len(indv) >= 1:
        print('Sending Mail')
        htmlrow1 = ""
        htmlrow2 = ""
        htmlrow3 = ""
        htmlrow4 = ""
        htmlrow5 = ""
        htmlrow6 = ""
        htmlrow7 = ""
        htmlrow8 = ""
        for d in indv:
            htmlrow1 = htmlrow1+"<td>" + str(d[0])+"</td>"
            htmlrow2 = htmlrow2+"<td>" + str(d[1])+"</td>"
            htmlrow3 = htmlrow3+"<td>" + str(d[2])+ "</td>"
            htmlrow4 = htmlrow4+"<td>" + str(d[3]) + "</td>"
            htmlrow5 = htmlrow5+"<td>" + str(d[4]) + "</td>"
            htmlrow6 = htmlrow6+"<td>" + str(d[5]) + "</td>"
            htmlrow7 = htmlrow7+"<td>" + str(d[6]) + "</td>"
            htmlrow8 = htmlrow8+"<td>" + str(d[7]) + "</td>"
        table_invd = "<tr style = 'background-color: #afd4ea'><td></td>"+htmlrow1+"</tr><tr><td>12 hours</td>"+htmlrow2+"</tr><tr><td>24 hours</td>"+htmlrow3+"</tr><tr><td>48 Hours</td>"+htmlrow4+"</tr><tr><td>72 Hours</td>"+htmlrow5+"</tr><tr><td>Above 72 Hours</td>"+htmlrow6+"</tr><tr><td left; colspan='12'></td></tr><tr><td>Arrived Items</td>"+htmlrow8+"</tr><tr><td>Arrival TAT (Days)</td>"+htmlrow7+"</tr>"
        htmlrow1 = ""
        htmlrow2 = ""
        htmlrow3 = ""
        htmlrow4 = ""
        htmlrow5 = ""
        htmlrow6 = ""
        htmlrow7 = ""
        htmlrow8 = ""
        for d in indv_mtd:
            htmlrow1 = htmlrow1+"<td>" + str(d[0])+"</td>"
            htmlrow2 = htmlrow2+"<td>" + str(d[1])+"</td>"
            htmlrow3 = htmlrow3+"<td>" + str(d[2])+ "</td>"
            htmlrow4 = htmlrow4+"<td>" + str(d[3]) + "</td>"
            htmlrow5 = htmlrow5+"<td>" + str(d[4]) + "</td>"
            htmlrow6 = htmlrow6+"<td>" + str(d[5]) + "</td>"
            htmlrow7 = htmlrow7+"<td>" + str(d[6]) + "</td>"
            htmlrow8 = htmlrow8+"<td>" + str(d[7]) + "</td>"
        table_invd_mtd = "<tr style = 'background-color: #afd4ea' ><td></td>"+htmlrow1+"</tr><tr><td>12 hours</td>"+htmlrow2+"</tr><tr><td>24 hours</td>"+htmlrow3+"</tr><tr><td>48 Hours</td>"+htmlrow4+"</tr><tr><td>72 Hours</td>"+htmlrow5+"</tr><tr><td>Above 72 Hours</td>"+htmlrow6+"</tr><tr><td left; colspan='12'></td></tr><tr><td>Arrived Items</td>"+htmlrow8+"</tr><tr><td>Arrival TAT (Days)</td>"+htmlrow7+"</tr>"
        
        fromaddr = "Procurement Reporting <team.procurement>"
        toaddr = []
        tocc = []
        #toaddr = ['harpreet.kumar']
        #tocc = ['harpreet.kumar']
        now = datetime.datetime.now()
        yest = now - datetime.timedelta(1)
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ", ".join(toaddr)
        msg['CC'] = ", ".join(tocc)
        msg['Subject'] = "Dubai Procurement " + yest.strftime("%d-%b") + " | MTD in 48 hrs : "+ MTD[0][2]
        body = """ <html>
                    <body>
                    <p>Hi Team,</p>
                    <p>Please find below details regarding this month performance:</p>

                    <p><b><u>Overall MTD:</u></b></p>
                    <table border = 1 cellpadding = 5 cellspacing =0>
                    <tr style = "background-color: #afd4ea">
                    <th text-align: left; colspan='2' >% Arrival(JIT)</th>
                    <th text-align: center>Targets</th>
                    </tr><tr><td>12 Hours</td><td>"""+ MTD[0][0]+"""</td><td>30%</td></tr>
                    <tr><td>24 Hours</td><td>"""+ MTD[0][1]+"""</td><td>60%</td></tr>
                    <tr><td>48 Hours</td><td>"""+ MTD[0][2]+"""</td><td>75%</td></tr>
                    <tr><td>72 Hours</td><td>"""+ MTD[0][3]+"""</td><td>85%</td></tr>
                    <tr><td>Above 72 Hours</td><td>"""+ MTD[0][4]+"""</td><td>85% +</td></tr>
                    <tr><td colspan='3'></td></tr>
                    <tr><td>Arrived Items</td><td style = "text-align: center" colspan="2">"""+ str(MTD[0][6])+"""</td></tr>
                    <tr><td>Arrival TAT (Days) </td><td style = "text-align: center" colspan="2">"""+ str(MTD[0][5])+"""</td></tr>
                    </table>
                    
                    <p><b><u>Individual MTD:</u></b></p>
                    <table border = 1 cellpadding = 5 cellspacing =0>
                    """+ table_invd_mtd +"""</table>

                    <p><b><u>Individual Yesterday:</u></b></p>
                    <table border = 1 cellpadding = 5 cellspacing =0>
                    """+ table_invd +"""</table>
                    
                    <p>Regards,<br>
                    Proc reporting</p>
                    <p>This is an automated report. Please contact harpreet.kumar for any query.</p>
                    </body></html>"""
        msg.attach(MIMEText(body, 'html'))
        filename = "DXB_Arrival_yesterday.csv"
        attachment = open("DXB_Arrival_yesterday.csv", "r")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('user_id', "Password")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr + tocc, text)
        print('Mail Sent!!!...')
        server.quit()

def main():
    try:
        ksa_arrival_report()
        dxb_arrival_report()
        
    except Exception as Err:
        print(Err)

if __name__ == "__main__":
    main()
