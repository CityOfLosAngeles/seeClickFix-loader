# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 11:23:21 2017

@author: Cerina
"""

#import json
import sys
import requests
import gspread

from oauth2client.service_account import ServiceAccountCredentials
scope = "https://spreadsheets.google.com/feeds"

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gs = gspread.authorize(credentials)

year = sys.argv[1]
sheetName = sys.argv[2]

mySheet = gs.open(sheetName).sheet1   

mySheet.clear()
mySheet.resize(1, 26)

def loadPage(page):
    aPage = str(page)
    
    rstring = 'https://seeclickfix.com/open311/v2/670/requests.json?start_date=' + \
    str(year) + '-01-01T00:00:00Z&end_date=' + str(int(year) + 1) + \
    '-01-01T00:00:00Z&page=' + aPage + '&per_page=100'

    
    r = requests.get(rstring)
    
    if len(r.json()) == 0:
        return 0
    else:
        #sheet_data is a list of dictionaries
        sheet_data = r.json()
        #sheet_data = sorted(sheet_data, key = lambda k: k["service_request_id"])
        
        #header_list is list of cell objects
        columnnumber = 0
        header_list = mySheet.range(1, 1, 1, len(r.json()[0]))
        for i in r.json()[0].keys():
            header_list[columnnumber].value = i
            columnnumber += 1
        
        newSheetStartIndex = 0
        
        #If spreadsheet is has empty first row
        if mySheet.get_all_values() == []:
            oldSheet = []
        
        #If spreadsheet has data--
        #1. Sheet has headers plus value data
        elif len(mySheet.get_all_records()) != 0:
            #make a list of dictionary of all the records
            oldSheet = mySheet.get_all_records() 
            #Look at the last "requested_datetime" value
            last_id = oldSheet[mySheet.row_count -2]["service_request_id"]
            last_rowNum_oldSheet = len(oldSheet) + 1 
        
            #Look at each row in sheet_data, keeping track of the row number.
            #If sheet_data's "requested_timedate" field matches last_time, split sheet_data
            #at that row and update sheet_data
            if len(sheet_data) != 0:
                for i in range(len(sheet_data)):
                    if last_id == sheet_data[i]["service_request_id"]:
                        newSheetStartIndex = i + 1
            
                   
        #2. Sheet only has header, no data
        else:
            oldSheet = []
            
          
        sheet_data = sheet_data[newSheetStartIndex:]
        
        sheet_data_vals = []
        
        #sheet_data_vals is a list of lists
        for i in range(len(sheet_data)):
            sheet_data_vals.append(list(sheet_data[i].values()))
            
        
        #Resize google sheet to fit the data, including a row for the headers
        mySheet.resize(len(oldSheet + sheet_data_vals)+1, mySheet.col_count)
        
        #cell_matrix is a list of cell objects
        cell_matrix = []
        cell_matrix = cell_matrix + header_list
        
        
        #Make rownumber reflective of the newest row
        rownumber = len(oldSheet) + 2
        
        
        #Each row in sheet_data represents a list, where each list holds the values
        for row in sheet_data_vals:
            #cellrange = 'A{row}:{letter}{row}'.format(row=rownumber, letter=chr(len(row) + ord('a') - 1))
            # get the row from the worksheet
            #cell_list is list of cell objects 
            cell_list = mySheet.range(rownumber, 1, rownumber, len(sheet_data_vals[0]))
            columnnumber = 0
            #cell represents individual value from the row list
            for cell in row:
                #cell_list updated with values from row
                cell_list[columnnumber].value = row[columnnumber]
                columnnumber += 1
            # add the cell_list, which represents all cells in a row to the full matrix
            cell_matrix = cell_matrix + cell_list
            rownumber += 1
        # output the full matrix all at once to the worksheet.
        
        mySheet.update_cells(cell_matrix)
        
        return 1


thisPage = 1
    
while loadPage(thisPage) != 0:
    thisPage += 1

