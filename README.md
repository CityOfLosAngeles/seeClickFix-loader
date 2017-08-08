# seeClickFix-loader
Automate the reading of SeeClickFix Requests into formats that allow staff to add to the myLA 311 CRM 


## Before running the program:
To programmatically access your spreadsheet, you’ll need to create a service account and OAuth2 credentials from the Google API Console.


1.	Open a google spreadsheet in your google drive. Name it what you want, but remember the name. You will use it later.
2.	Go to the Google APIs Console
3.	Create a new project.
4.	Click Enable API. Search for and enable the Google Drive API.
5.	Create credentials for a Web Server to access Application Data.
6.	Name the service account and grant it a Project Role of Editor.
7.	Download the JSON file.
8.	Copy the JSON file to your code directory and rename it to \client_secret.json\
9.  Find the client_email inside client_secret.json. Back in your spreadsheet, click the Share button in the top right, unclick the Notify people check box, and paste the client email into the People field to give it edit rights. Hit Send.
(See https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html for more details)


## Running the program:
From terminal, change director to the location of `SCF.py`
Run: `SCF.py (year of the records you want) (“Name of the spreadsheet inside quotes”)`
The spreadsheet will start updating

Once spreadsheet is finished updating, you can sort the sheet according to the field of your choosing. In the spreadsheet, click on the column you want to sort by. On the menu, click Data  Sort Range. Check the “Data has header row” checkbox, then choose the radio button of whether you want to sort in order, or reverse order. Finally, click the blue sort button.
