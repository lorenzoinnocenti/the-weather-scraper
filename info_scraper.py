import requests
import csv
import lxml.html as lh
import time
import config
from bs4 import BeautifulSoup
from util.UnitConverter import ConvertToSystem
from util.Parser import Parser
from util.Utils import Utils
import json
import re
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta


# configuration
stations_file = open('stations_milan.txt', 'r')
URLS = stations_file.readlines()
timeout = 5
sleeptime = 5
file_name = 'station_info_milan'
folder_name = 'csv'
fieldnames = ['stationName',
              'neighborhood', 
              'name',
              'city',	
              'state',	
              'country',	
              'latitude',	
              'longitude',	
              'elevation',	
              'height',	
              'stationType',	
              'surfaceType',	
              'tzName']

def scrap_info(URLS):
    csv_path = folder_name+'/'+file_name+'.csv'
    with open(csv_path, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        row_dict = {}
        for field in fieldnames:
            row_dict[field] = field
        writer.writerow(row_dict)
        session = requests.Session()
        for i, url in enumerate(URLS): 
            url = url.strip('\n')
            url = url.strip(' ')
            print('Scraping data from '+url)
            connected = False
            while not connected:
                try:
                    html = session.get(url, timeout=timeout) 
                    connected = True
                except Exception as e:
                    print(e)
                    connected = False
                    print("refreshing session")
                    time.sleep(sleeptime)
                    session = requests.Session()
            soup = BeautifulSoup(html.text, 'html.parser')
            txt = soup.find('script', id="app-root-state").string
            parsed = re.split(';|,|&q|:', txt)
            parsed_noempty = [x for x in parsed if x != '']
            row_dict = {}
            row_dict['stationName'] = url.split('/')[-1]
            for i, field in enumerate(fieldnames[1:]):
                try: 
                    row_dict[field] = parsed_noempty[parsed_noempty.index(field)+1]
                except Exception as e:
                    row_dict[field] = 'missing'
                if row_dict[field] in fieldnames: 
                    row_dict[field] = 'missing'
            if row_dict['state'] == 'country':
                row_dict['state'] = 'missing'
            writer.writerow(row_dict)
            csvfile.flush()

if __name__ == '__main__':
    scrap_info(URLS)