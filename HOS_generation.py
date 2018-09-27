from oauth2client.service_account import ServiceAccountCredentials
import gspread
import xlwings as xl

def hos_update():
    try:
        wb = xl.Book.caller()
        SCOPES = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('E:\Proc_Reports\wadicredentials.json', SCOPES)
        gc = gspread.authorize(credentials)
        workbook = gc.open_by_key('1G0RsL1Ws_L1HdlGh7t4t40WmaxKQezkd6marmycxDsw')
        worksheets = workbook.worksheet('HOS Generation')
        col1 = worksheets.get_all_values()
        xl.sheets('Seller_Details').range('A1').value = col1
        wb.save()
    except:
        quit()
