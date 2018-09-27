#/usr/bin/python2
from Scripts.Connection import mysql_server, gsheet_connect

ss = gsheet_connect("1tpN6t3Dq_WnbR9udFPLl0VUb2vM_piekK0wvN5LPn_U")
sheet = ss.worksheet_by_title("control_panel")
live_beauty = sheet.get_value("E1")
data_beauty = mysql_server("reporting", live_beauty)
data_beauty = [list(i) for i in data_beauty]

live_elect = sheet.get_value("H1")
data_elect = mysql_server("reporting", live_elect)
data_elect = [list(i) for i in data_elect]

ss.worksheet_by_title("beauty_summary").clear(start='A2', end="F2570")
ss.worksheet_by_title("beauty_summary").update_cells("A2", data_beauty)

ss.worksheet_by_title("elect_summary").clear(start='A2', end="F1000")
ss.worksheet_by_title("elect_summary").update_cells("A2", data_elect)
