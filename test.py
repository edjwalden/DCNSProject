import PySimpleGUI as sg
import csv
import os
from datetime import datetime

'''
### GRABS TIME ###
now = datetime.now()
currenttime = now.strftime('%d/%m/%Y at %H:%M:%S')
'''

### Sets default directory ###
os.chdir('c:/Users/Ed/Documents/VSCODE/Tutorial/Python/Messing around/GUI/')

### Creates CSV file for accounts if it does not exist ###
if os.path.exists('accounts.csv') == False:
    with open('accounts.csv', 'w', newline='') as accountsfile:
        writer = csv.writer(accountsfile)
        writer.writerow(['Admin','password123', 'Admin']) # Creates admin account as default
        writer.writerow(['Technician','password123', 'Technician'])
        writer.writerow(['User','password123', 'User'])

### Creates CSV file for tickets if it does not exist ###
if os.path.exists('tickets.csv') == False:
    now = datetime.now()
    currenttime = now.strftime('%d/%m/%Y at %H:%M:%S')
    with open('tickets.csv', 'w', newline='') as ticketfile:
        writer = csv.writer(ticketfile)
        #writer.writerow([ID,ISSUETYPE,DIVISION,NAME,PRIORITY,DESCRIPTION,STATUS,COMMMENTS, TIME SUBMITTED])
        writer.writerow(['1', 'Hardware', 'Finance', 'Dave Hurley', 'High', 'Pc stopped working.','Pending','',currenttime])
        writer.writerow(['2', 'Software', 'Acquisitions', 'Waldebert Kalpana', 'Low', 'Antivirus crashed.','Pending','',currenttime])
        writer.writerow(['3', 'Hardware', 'IT', 'Starr Mitar', 'Low', 'Lost my charger.','Pending','',currenttime])
        writer.writerow(['4', 'Hardware', 'Recruitment', 'User', 'Low', 'Lost my shoes.','Pending','',currenttime])

### INITIALISES TICKET TABLE
global tickettabledata
global tableheaders
tickettabledata = []
tableheaders = ['ID','Issue Type','Division','Name','Priority','Description','Status','Comments','Time Created']
with open('tickets.csv', 'r') as ticketfile: # Takes CSV data and puts it into a table
    reader = csv.reader(ticketfile)
    for row in reader:
        tickettabledata.append(row)  


### INITIALISES THEME
new_theme = {"BACKGROUND": '#94999d', "TEXT": '#FFFFFF', "INPUT": sg.COLOR_SYSTEM_DEFAULT, 
             "TEXT_INPUT": sg.COLOR_SYSTEM_DEFAULT, "SCROLL": sg.COLOR_SYSTEM_DEFAULT,
             "BUTTON": ['#ffffff','#66747f'], "PROGRESS": sg.COLOR_SYSTEM_DEFAULT, "BORDER": 0.1,
             "SLIDER_DEPTH": 0, "PROGRESS_DEPTH": 0
             }
sg.theme_add_new('MyTheme', new_theme)
sg.theme('MyTheme')
themefont = ('Verdana', 10)
sg.set_options(font=themefont)



### TEMPLATE for new windows ###
def DefaultWindow():
    layout = [[]] 

    window = sg.Window('Default', layout) 

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.Close()

### LOGIN window ###
def Main():
    layout = [[sg.Text('Please enter your details')],
              [sg.Text('Username'), sg.Stretch(), sg.Input(key='-USERNAME-',size=(30,1))],
              [sg.Text('Password'), sg.Stretch(), sg.Input(key='-PASSWORD-',size=(30,1))],
              [sg.Button('Login', key='-LOGIN-'), sg.Button('Admin Login', key='-ADMINLOGIN-'), sg.Stretch(), sg.Button('Create Account', key='-CREATE-')],
              [sg.Button('Open Account CSV', key= '-OPENACCOUNTCSV-'), sg.Stretch(), sg.Button('Open Ticket CSV', key= '-OPENTICKETCSV-')]
            ]

    window = sg.Window('Login', layout)

    while True:
        event, values = window.read()
        if event == 'Quit' or event == sg.WIN_CLOSED:
            break
        if event == '-LOGIN-':
            global username
            global password
            username = str(values['-USERNAME-'])
            password = str(values['-PASSWORD-'])
            with open('accounts.csv', 'r') as accountsfile:
                reader = csv.reader(accountsfile)
                for row in reader:
                    if row[0] == username and row[1] == password: # Checks all rows in csv file, if username and password match, condition is true.
                        global userprivilege
                        userprivilege = row[2]
                        window.Close()
                        OptionWindow(username, userprivilege)
        if event == '-ADMINLOGIN-':
            username = "Admin"
            userprivilege = "Admin"
            window.Close()
            OptionWindow("Admin", "Admin") #LOGS IN AS ADMIN
        if event == '-OPENACCOUNTCSV-':
            os.startfile('accounts.csv')
        if event == '-OPENTICKETCSV-':
            os.startfile('tickets.csv')
        if event == '-CREATE-':
            CreateAccountPage()

### SPLASH/HOME SCREEN ###
### Takes args from Main() ###
def OptionWindow(Username,UserPriv):
    match UserPriv:
        case "User":
            layout = [[sg.Text('Hello, ' + Username + ", your privilege is " + UserPriv)],
                      [sg.Button('Create Ticket', key='-NEWTICKET-')],
                      [sg.Button('Manage Tickets', key='-MANAGETICKET-')],
                      [sg.Stretch(),sg.Button('Back')]
                      ]
        case "Technician":
            layout = [[sg.Text('Hello, ' + Username + ", your privilege is " + UserPriv)],
                      [sg.Button('Create Ticket', key='-NEWTICKET-')],
                      [sg.Button('Manage Tickets', key='-MANAGETICKET-')],
                      [sg.Stretch(),sg.Button('Back')]
                      ]
        case "Admin":
            layout = [[sg.Text('Hello, ' + Username + ", your privilege is " + UserPriv)],
                      [sg.Button('Create Ticket', key='-NEWTICKET-')],
                      [sg.Button('Manage Tickets', key='-MANAGETICKET-')],
                      [sg.Button('Manage Users', key= '-MANAGEUSERS-')],
                      [sg.Stretch(),sg.Button('Back')]
                      ]

    window = sg.Window('Home', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Back':
            window.Close()
            Main()    
        if event == '-MANAGETICKET-':
            ManageTickets()
        if event == '-NEWTICKET-':
            NewTicket()
    window.Close()

### Screen to create accounts ###
def CreateAccountPage():
    layout = [[sg.Text('New Username: '), sg.Stretch(), sg.Input(key='-NEWUSER-', size= (30,1))],
              [sg.Text('New Password: '), sg.Stretch(),sg.Input(key='-NEWPASS-', size= (30,1))],
              [sg.Button('Create account', key='-CREATEACCOUNT-'), sg.Text('', key='-CONFIRM-'), sg.Stretch(), sg.DropDown(values=('User','Technician','Admin'),key='-PRIVILEGE-', size= (9,1), default_value="User")]
              ]

    window = sg.Window('Create an Account', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-CREATEACCOUNT-':
            newuser = str(values['-NEWUSER-'])
            newpass = str(values['-NEWPASS-'])
            match = 0
            with open('accounts.csv', 'r') as accountsfile: # checks if username currently exists.
                reader = csv.reader(accountsfile)
                for row in reader:
                    if row[0] == newuser:
                        match = 1
                        window['-CONFIRM-'].update("Account already exists. Did not create")
            if match == 0 and newuser != "" and newpass != "":
                with open('accounts.csv', 'a', newline='') as accountsfile: # If username does not exist.
                    writer = csv.writer(accountsfile) # Creates account
                    writer.writerow([newuser,newpass,str(values['-PRIVILEGE-'])])
                window['-CONFIRM-'].update("Created")
    window.Close()

### Screen to manage/select tickets ###
def ManageTickets():
    
    UserTicketTable = []
    if userprivilege == "User":
        for rows in tickettabledata:
            if rows[3] == username:
                UserTicketTable.append(rows)
        TicketTable = sg.Table(values=UserTicketTable, headings= tableheaders, # DEFINE TABLE
                           auto_size_columns=True,
                           justification='centre', key='-TABLE-',
                           selected_row_colors='black on #51b4db',
                           enable_click_events=True,
                           enable_events=True,
                           visible_column_map=[True,True,True,True,True,True,True,False,True] # Makes comments invisible
                           )
    else:
        TicketTable = sg.Table(values=tickettabledata, headings= tableheaders, # DEFINE TABLE
                            auto_size_columns=True,
                            justification='centre', key='-TABLE-',
                            selected_row_colors='black on #51b4db',
                            enable_click_events=True,
                            enable_events=True,
                            visible_column_map=[True,True,True,True,True,True,True,False,True] # #Makes comments invisible
                            )

    layout = [[TicketTable],
              [sg.Button('Open Ticket', key='-OPENTICKET-'), sg.Stretch(), sg.Button('Back', key='-BACK-')]]

    window = sg.Window('Manage Tickets', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-OPENTICKET-' and values['-TABLE-'] != []: #If button pressed and item clicked
            thiscase = int(values['-TABLE-'][0]) ## Takes index value of DISPLAYED table - This is so users can open the correct ticket (display index ID != caseid when user's table is displayed.)

            if userprivilege == 'User': 
                caseid = int(UserTicketTable[thiscase][0])-1 
            else:
                caseid = int(tickettabledata[thiscase][0])-1
            window.Close()
            ControlTicket(caseid)
        if event == '-BACK-':
            window.Close()

    window.Close()

### Screen to control tickets ###
### Takes args from ManageTickets() ###
def ControlTicket(caseid):
    # Field Headings
    # 0: ID
    # 1: ISSUETYPE
    # 2: DIVISION
    # 3: NAME
    # 4: PRIORITY
    # 5: DESCRIPTION
    # 6: STATUS
    # 7: COMMENTS
    # 8: TIME SUBMITTED

    CurrentTicket = tickettabledata[caseid]

    if userprivilege == 'User': # USER CANNOT CHANGE STATUS
        now = datetime.now()
        currenttime = now.strftime('%d/%m/%Y at %H:%M:%S')
        layout = [[sg.Text('Ticket ID: ' + CurrentTicket[0]), sg.Stretch(), sg.Text('Name of ticket submitter: ' + CurrentTicket[3])],
                [sg.HSeparator(pad=(10,0))],
                [sg.Text('Issue type: ' + CurrentTicket[1]), sg.Stretch(), sg.Text('Priority: ' + CurrentTicket[4])],
                [sg.HSeparator(pad=(10,0))],
                [sg.Text('Division: ' + CurrentTicket[2]), sg.Stretch(), sg.Text('Status: ' + str(CurrentTicket[6]), key='-STATUS-')],
                [sg.HSeparator(pad=(10,0))],
                [sg.Text('Description: '+ CurrentTicket[5]), sg.Stretch(), sg.Text('Ticket Created: ' + CurrentTicket[8])],
                [sg.HSeparator(pad=(10,0))],
                [sg.Text('Comments:'),sg.Text('',key='-CONFIRM-')],
                [sg.Multiline(default_text=CurrentTicket[7],size=(60, 10),key='-COMMENTS-')],
                [sg.Button('Save', key='-SAVE-'), sg.Button('Save and exit', key='-SAVEANDEXIT-'), sg.Stretch(), sg.Button('Back',key='-BACK-')]
                ]
    else:
        now = datetime.now()
        currenttime = now.strftime('%d/%m/%Y at %H:%M:%S')
        layout = [[sg.Text('Ticket ID: ' + CurrentTicket[0]), sg.Stretch(), sg.Text('Name of ticket submitter: ' + CurrentTicket[3])],
                [sg.HSeparator(pad=(10,0))],
                [sg.Text('Issue type: ' + CurrentTicket[1]), sg.Stretch(), sg.Text('Priority: ' + CurrentTicket[4])],
                [sg.HSeparator(pad=(10,0))],
                [sg.Text('Division: ' + CurrentTicket[2]), sg.Stretch(), sg.Text('Status: '), sg.DropDown(values=('Pending','Active','Resolved','Escalated','Re-opened'), default_value=CurrentTicket[6], key='-STATUS-')],
                [sg.HSeparator(pad=(10,0))],
                [sg.Text('Description: '+ CurrentTicket[5]), sg.Stretch(), sg.Text('Ticket Created: ' + CurrentTicket[8])],
                [sg.HSeparator(pad=(10,0))],
                [sg.Text('Comments:'),sg.Text('',key='-CONFIRM-')],
                [sg.Multiline(default_text=CurrentTicket[7],size=(60, 10),key='-COMMENTS-')],
                [sg.Button('Save', key='-SAVE-'), sg.Button('Save and exit', key='-SAVEANDEXIT-'), sg.Stretch(), sg.Button('Back',key='-BACK-')]
                ]
               
    window = sg.Window('Edit Ticket', layout) 

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '-BACK-':
            break
        
        if event == '-SAVE-':
            now = datetime.now()
            currenttime = now.strftime('%d/%m/%Y at %H:%M:%S')
            if userprivilege == 'User':
                CaseDetails = [CurrentTicket[0],CurrentTicket[1],CurrentTicket[2],CurrentTicket[3],CurrentTicket[4],CurrentTicket[5],CurrentTicket[6],str(values['-COMMENTS-'] + '\n-- Update to ticket made on ' + str(currenttime) + ' by '+ username + ' --\n'),CurrentTicket[8]]
            else:
                CaseDetails = [CurrentTicket[0],CurrentTicket[1],CurrentTicket[2],CurrentTicket[3],CurrentTicket[4],CurrentTicket[5],str(values['-STATUS-']),str(values['-COMMENTS-'] + '\n-- Update to ticket made on ' + str(currenttime) + ' by '+ username + ' --\n'),CurrentTicket[8]]
            with open('tickets.csv', 'w', newline='') as ticketfile: # Appends the ticket CSV 
                writer = csv.writer(ticketfile)
                for row in tickettabledata:                          # Rewrites the whole CSV
                    if int(row[0])-1 == caseid:                      # If current ticket, writes casedetails
                        writer.writerow(CaseDetails)                
                    else:
                        writer.writerow(tickettabledata[int(row[0])-1]) # Else writes what is in tickettabledata
            with open('tickets.csv', 'r') as ticketfile:            # Updates ticket data for the app
                    reader = csv.reader(ticketfile)
                    tickettabledata.clear()
                    for row in reader:                               
                        tickettabledata.append(row)
            window['-CONFIRM-'].update("Saved.")
            window['-COMMENTS-'].update(CaseDetails[7])             # Refreshes comments box upon saving
        
        if event == '-SAVEANDEXIT-':
            now = datetime.now()
            currenttime = now.strftime('%d/%m/%Y at %H:%M:%S')
            CaseDetails = [CurrentTicket[0],CurrentTicket[1],CurrentTicket[2],CurrentTicket[3],CurrentTicket[4],CurrentTicket[5],values['-STATUS-'],str(values['-COMMENTS-'] + '\n-- Update to ticket made on ' + str(currenttime) + ' by '+ username + ' --\n'),CurrentTicket[8]]
            with open('tickets.csv', 'w', newline='') as ticketfile: # Appends the ticket CSV 
                writer = csv.writer(ticketfile)
                for row in tickettabledata:                          # Rewrites the whole CSV
                    if int(row[0])-1 == caseid:                      # If ID = current ticket, writes current ticket's details to CSV row.
                        writer.writerow(CaseDetails)                
                    else:
                        writer.writerow(tickettabledata[int(row[0])-1]) # Else writes what is in tickettabledata
            with open('tickets.csv', 'r') as ticketfile:            # Updates ticket data for the app
                    reader = csv.reader(ticketfile)
                    tickettabledata.clear()
                    for row in reader:                               
                        tickettabledata.append(row)
            break
    window.Close()
    ManageTickets()

### Screen to make new tickets
def NewTicket():

    # Field Headings
    # 0: ID
    # 1: ISSUETYPE
    # 2: DIVISION
    # 3: NAME
    # 4: PRIORITY
    # 5: DESCRIPTION
    # 6: STATUS
    # 7: COMMENTS
    # 8: TIME SUBMITTED

    NewTicketID = len(tickettabledata) + 1
    layout = [[sg.Text("Ticket ID: " + str(NewTicketID))],
              [sg.Text("Issue Type: "), sg.Stretch(), sg.DropDown(values=("Hardware", "Software", "Other"), key='-ISSUETYPE-')],
              [sg.Text("Division: "), sg.Stretch(), sg.DropDown(values=("Finance", "Acquisitions", "IT", "Recruitment", "HR"), key='-DIVISION-')],
              [sg.Text("Name: "), sg.Stretch(), sg.Text(username)],
              [sg.Text("Priority: "), sg.Stretch(), sg.DropDown(values=("High", "Low"), key='-PRIORITY-')],
              [sg.Text("Describe your issue in more detail: ", size=(40,None))],
              [sg.Multiline(size=(35, 6),key='-DESCRIPTION-')],
              [sg.Button("Submit",key='-SUBMIT-'), sg.Text('', key='-CONFIRM-'), sg.Stretch(), sg.Button('Back', key='-BACK-')]
              ] 

    window = sg.Window('Create Ticket', layout, size=(300,300)) 

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-SUBMIT-':
            now = datetime.now()
            currenttime = now.strftime('%d/%m/%Y at %H:%M:%S')
            NewTicketID = len(tickettabledata) + 1
            CaseDetails = [NewTicketID, values['-ISSUETYPE-'], values['-DIVISION-'], username, values['-PRIORITY-'], values['-DESCRIPTION-'],'Pending','', currenttime]
            with open('tickets.csv', 'a', newline='') as ticketfile: # Appends the ticket CSV
                writer = csv.writer(ticketfile)
                writer.writerow(CaseDetails)
            with open('tickets.csv', 'r') as ticketfile: # Updates ticket data for the app
                    reader = csv.reader(ticketfile)
                    tickettabledata.clear()
                    for row in reader:
                        tickettabledata.append(row) 
            window['-CONFIRM-'].update("Ticket Logged")
            window['-SUBMIT-'].update(disabled=True) # Disables submit button until window closes
        if event == '-BACK-':
            break
    window.Close()

Main()