import json
import sys
import time
import datetime
import gspread
import psutil
import subprocess
from system_info import get_temperature
from oauth2client.service_account import ServiceAccountCredentials


GDOCS_OAUTH_JSON       = 'rpidata-8b0cc4383ebd.json'
GDOCS_SPREADSHEET_NAME = 'rpidata'
FREQUENCY_SECONDS      = 1
def login_open_sheet(oauth_key_file, spreadsheet):
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, 
                      scopes = ['https://spreadsheets.google.com/feeds',
                                'https://www.googleapis.com/auth/drive'])
        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet. Check OAuth credentials, spreadsheet name, and')
        print('make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)
def send_to_googleSheets(name):
    worksheet = None
    if worksheet is None:
        worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
    dat = datetime.datetime.now()
    cpu = psutil.cpu_percent()
    tmp = get_temperature()
    print(dat)
    print('CPU Usage in %: '+str(cpu))
    print('Temperature in C: ' +str(tmp))
    print('Detect '+str(len(name))+' person')
    
    if(len(name)==1):
        
        try:
            worksheet.append_row((str(dat), cpu, tmp,name[0]))
            print('name is:'+name[0])
        except:
            print('Append error, logging in again')
            worksheet = None
            time.sleep(FREQUENCY_SECONDS)
    if(len(name)==2):
        
        try:
            print('name is:'+name[0]+' and '+name[1])
            worksheet.append_row((str(dat), cpu, tmp,name[0],name[1])) 
        except:
            print('Append error, logging in again')
            worksheet = None
            time.sleep(FREQUENCY_SECONDS)
    print('Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME))
    time.sleep(FREQUENCY_SECONDS)
    
if __name__=='__main__':
    send_to_googleSheets()
