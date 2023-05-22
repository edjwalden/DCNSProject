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
#directory = 'c:/Users/Ed/Documents/VSCODE/Tutorial/Python/Messing around/GUI/'
directory = os.path.dirname(os.path.abspath(__file__)) ## sets directory to folder containing running script file.
os.chdir(directory)

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

### INITIALISES TICKET TABLE FROM TICKETS.CSV
global tickettabledata
global tickettableheaders
tickettabledata = []
tickettableheaders = ['ID','Issue Type','Division','Name','Priority','Description','Status','Comments','Time Created']

def RefreshTicketTable():
    with open('tickets.csv', 'r') as ticketfile: # Takes CSV data and puts it into a table
        tickettabledata.clear()
        reader = csv.reader(ticketfile)
        for row in reader:
            tickettabledata.append(row)

### INITIALISES ACCOUNT TABLE FROM ACCOUNTS.CSV
global accounttabledata
global accountableheaders
accounttabledata = []
accountableheaders = ['Username', 'Password', 'Privilege']

def RefreshAccountTable():
    with open('accounts.csv','r') as accountsfile: # REFRESHES INTERNAL ACCOUNTS TABLE DATA
        accounttabledata.clear()                   
        reader = csv.reader(accountsfile)
        for row in reader:
            accounttabledata.append(row)

def RewriteTicketCSV(CaseDetails, caseid):
    with open('tickets.csv', 'w', newline='') as ticketfile: # Rewrites the ticket CSV with one row changed
        writer = csv.writer(ticketfile)
        for row in tickettabledata:                          # Rewrites the whole CSV line by line
            if int(row[0])-1 == caseid:                      # If ID = current ticket, writes current ticket's details to CSV row.
                writer.writerow(CaseDetails)                
            else:
                writer.writerow(tickettabledata[int(row[0])-1]) # Else writes what is in tickettabledata


### INITIALISES THEME AND FONT
new_theme = {"BACKGROUND": '#94999d', "TEXT": '#FFFFFF', "INPUT": sg.COLOR_SYSTEM_DEFAULT, 
             "TEXT_INPUT": sg.COLOR_SYSTEM_DEFAULT, "SCROLL": sg.COLOR_SYSTEM_DEFAULT,
             "BUTTON": ['#ffffff','#66747f'], "PROGRESS": sg.COLOR_SYSTEM_DEFAULT, "BORDER": 0.1,
             "SLIDER_DEPTH": 0, "PROGRESS_DEPTH": 0
             }
sg.theme_add_new('MyTheme', new_theme)
sg.theme('MyTheme')
themefont = ('Verdana', 10)
sg.set_options(font=themefont)
'''
### TEMPLATE for new windows ###
def DefaultWindow():
    layout = [[]] 

    window = sg.Window('Default', layout) 

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.Close()
'''

### LOGIN window ####
def Main():
    menu_def = [['File',['Open Folder Location','Open Accounts CSV','Open Tickets CSV']]]

    layout = [[sg.Menu(menu_definition=menu_def, key='k')],
              [sg.Stretch(),sg.Text('Please enter your details:'),sg.Stretch()],
              [sg.Text('Username',pad=0), sg.Stretch(), sg.Input(key='-USERNAME-',size=(30,1))],
              [sg.Text('Password',pad=0), sg.Stretch(), sg.Input(key='-PASSWORD-',size=(30,1))],
              [sg.Button('Login', key='-LOGIN-'), sg.Button('Admin Login', key='-ADMINLOGIN-'), sg.Stretch(), sg.Button('Create Account', key='-CREATE-')],
              [sg.Text(os.getcwd())]
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
            with open('accounts.csv', 'r') as accountsfile:       # Compares entered credentials to account CSV file #
                reader = csv.reader(accountsfile)
                for row in reader:
                    if row[0] == username and row[1] == password: # Checks all rows in csv file, if username and password match, condition is true.
                        global userprivilege                      # Establishes privilege for the user globally.
                        userprivilege = row[2]
                        window.Close()
                        OptionWindow(username, userprivilege)
        if event == '-ADMINLOGIN-':
            username = "Admin"
            userprivilege = "Admin"
            window.Close()
            OptionWindow("Admin", "Admin") #LOGS IN AS ADMIN
        if event == 'Open Accounts CSV':
            os.startfile('accounts.csv')
        if event == 'Open Tickets CSV':
            os.startfile('tickets.csv')
        if event == 'Open Folder Location':
            os.startfile(directory)
        if event == '-CREATE-':
            CreateAccountPage()

### SPLASH/HOME SCREEN ###
### Takes args from Main() ###
def OptionWindow(Username,UserPriv):
    match UserPriv:                         ## Defines layouts depending on privilege
        case "User":                        
            layout = [[sg.Text('Hello, ' + Username + ", your privilege is " + UserPriv)],
                      [sg.Button('Create Ticket', key='-NEWTICKET-')],
                      [sg.Button('Manage Tickets', key='-MANAGETICKET-')],
                      [sg.Button('Manage Tickets New', key='-MANAGETICKET2-')],
                      [sg.Stretch(),sg.Button('Back')]
                      ]
        case "Technician":
            layout = [[sg.Text('Hello, ' + Username + ", your privilege is " + UserPriv)],
                      [sg.Button('Create Ticket', key='-NEWTICKET-')],
                      [sg.Button('Manage Tickets', key='-MANAGETICKET-')],
                      [sg.Button('Manage Tickets New', key='-MANAGETICKET2-')],
                      [sg.Stretch(),sg.Button('Back')]
                      ]
        case "Admin":
            layout = [[sg.Text('Hello, ' + Username + ", your privilege is " + UserPriv)],
                      [sg.Button('Create Ticket', key='-NEWTICKET-')],
                      [sg.Button('Manage Tickets', key='-MANAGETICKET-')],
                      [sg.Button('Manage Tickets New', key='-MANAGETICKET2-')],
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
        if event == '-MANAGETICKET2-':
            NewManageTickets()
        if event == '-NEWTICKET-':
            NewTicket()
        if event == '-MANAGEUSERS-':
            AccountsTablePage()
    window.Close()

### Screen to create accounts ###
def CreateAccountPage():
    layout = [[sg.Text('New Username: '), sg.Stretch(), sg.Input(key='-NEWUSER-', size= (30,1))],
              [sg.Text('New Password: '), sg.Stretch(),sg.Input(key='-NEWPASS-', size= (30,1))],
              [sg.Button('Create account', key='-CREATEACCOUNT-'), sg.Text('', key='-CONFIRM-'), sg.Stretch(), sg.DropDown(values=('User','Technician','Admin'),key='-PRIVILEGE-', size= (9,1), default_value="User",readonly=True)],
              [sg.Stretch(),sg.Button('Back')]
              ]

    window = sg.Window('Create an Account', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Back':
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
                RefreshAccountTable()
                window['-CONFIRM-'].update("Created")
    window.Close()

### Screen to manage/select tickets ###
def ManageTickets():
    
    UserTicketTable = []
    if userprivilege == "User":
        for rows in tickettabledata:
            if rows[3] == username:
                UserTicketTable.append(rows)
        TicketTable = sg.Table(values=UserTicketTable, headings= tickettableheaders, # DEFINE TABLE
                           auto_size_columns=True,
                           justification='centre', key='-TABLE-',
                           selected_row_colors='black on #51b4db',
                           enable_click_events=True,
                           enable_events=True,
                           visible_column_map=[True,True,True,True,True,True,True,False,True] # Makes comments invisible
                           )
    else:
        TicketTable = sg.Table(values=tickettabledata, headings= tickettableheaders, # DEFINE TABLE
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
        if event == '-OPENTICKET-' and values['-TABLE-'] != []:     ##If button pressed and item clicked
            thiscase = int(values['-TABLE-'][0])                    ## Takes index value of DISPLAYED table - This is so users can open the correct ticket)
                                                                    ## (display index ID != caseid when user's table is displayed. This is because the table only indexes items that are displayed
                                                                    ## This means users, who cannot see all tickets, have a different index list to the main ticket list
            if userprivilege == 'User': 
                caseid = int(UserTicketTable[thiscase][0])-1 
            else:
                caseid = int(tickettabledata[thiscase][0])-1
            window.Close()
            ControlTicket(caseid)
        if event == '-BACK-':
            window.Close()

    window.Close()

def NewManageTickets():
    #'ID','Issue Type','Division','Name','Priority','Description','Status','Comments','Time Created'
    UserTicketTable = []
    if userprivilege == "User":
        for rows in tickettabledata:
            if rows[3] == username:
                UserTicketTable.append(rows)
        TicketTable = sg.Table(values=UserTicketTable, headings= tickettableheaders, # DEFINE TABLE
                           auto_size_columns=True,
                           justification='centre', key='-TABLE-',
                           selected_row_colors='black on #51b4db',
                           enable_click_events=True,
                           enable_events=True,
                           visible_column_map=[False,True,False,True,True,False,True,False,False], # Makes comments invisible
                           expand_y=True
                           )
    else:
        TicketTable = sg.Table(values=tickettabledata, headings= tickettableheaders, # DEFINE TABLE
                            auto_size_columns=True,
                            justification='centre', key='-TABLE-',
                            selected_row_colors='black on #51b4db',
                            enable_click_events=True,
                            enable_events=True,
                            visible_column_map=[False,True,False,True,True,False,True,False,False], # #Makes comments invisible
                            expand_y=True
                            )
    
    previewcolumn = [[sg.Text("Name :", key='-DISPNAME-')],
                     [sg.Text('Description:', key='-DISPDESC-')]]

    layout = [[TicketTable, sg.VerticalSeparator(pad=(0)), sg.Column(previewcolumn, expand_y=True)],
              [sg.Button('Open Ticket', key='-OPENTICKET-'), sg.Stretch(), sg.Button('Back', key='-BACK-')]]

    window = sg.Window('Manage Tickets', layout, size=(800,280))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if values['-TABLE-'] != []:
            tableid = values['-TABLE-'][0]
            window['-DISPNAME-'].update('Name: %s' % tickettabledata[tableid][3])
            window['-DISPDESC-'].update('Description: %s' % tickettabledata[tableid][5])
        if event == '-OPENTICKET-' and values['-TABLE-'] != []: #If button pressed and item clicked
            thiscase = int(values['-TABLE-'][0])                    ## Takes index value of DISPLAYED table - This is so users can open the correct ticket )
                                                                    ## (display index ID != caseid when user's table is displayed. This is because the table only indexes items that are displayed
                                                                    ## This means users, who cannot see all tickets, have a different index list to the main ticket list
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
               
    window = sg.Window('Edit Ticket', layout, size=(500,350)) 

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
            RewriteTicketCSV(CaseDetails,caseid)
            RefreshTicketTable()
            window['-CONFIRM-'].update("Saved.")
            window['-COMMENTS-'].update(CaseDetails[7])             # Refreshes comments box upon saving
        
        if event == '-SAVEANDEXIT-':
            now = datetime.now()
            currenttime = now.strftime('%d/%m/%Y at %H:%M:%S')
            if userprivilege == 'User':
                CaseDetails = [CurrentTicket[0],CurrentTicket[1],CurrentTicket[2],CurrentTicket[3],CurrentTicket[4],CurrentTicket[5],CurrentTicket[6],str(values['-COMMENTS-'] + '\n-- Update to ticket made on ' + str(currenttime) + ' by '+ username + ' --\n'),CurrentTicket[8]]
            else:
                CaseDetails = [CurrentTicket[0],CurrentTicket[1],CurrentTicket[2],CurrentTicket[3],CurrentTicket[4],CurrentTicket[5],str(values['-STATUS-']),str(values['-COMMENTS-'] + '\n-- Update to ticket made on ' + str(currenttime) + ' by '+ username + ' --\n'),CurrentTicket[8]]
            RewriteTicketCSV(CaseDetails,caseid)
            RefreshTicketTable()
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
              [sg.Text("Issue Type: "), sg.Stretch(), sg.DropDown(values=("Hardware", "Software", "Other"), key='-ISSUETYPE-', readonly=True)],
              [sg.Text("Division: "), sg.Stretch(), sg.DropDown(values=("Finance", "Acquisitions", "IT", "Recruitment", "HR"), key='-DIVISION-', readonly=True)],
              [sg.Text("Name: "), sg.Stretch(), sg.Text(username)],
              [sg.Text("Priority: "), sg.Stretch(), sg.DropDown(values=("High", "Low"), key='-PRIORITY-', readonly=True)],
              [sg.Text("Describe your issue in more detail: ", size=(40,None))],
              [sg.Multiline(size=(35, 6),key='-DESCRIPTION-',)],
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
            RefreshTicketTable()
            window['-CONFIRM-'].update("Ticket Logged")
            window['-SUBMIT-'].update(disabled=True) # Disables submit button until window closes
        if event == '-BACK-':
            break
    window.Close()

### Screen for account table
def AccountsTablePage():
    AccountTable = sg.Table(values=accounttabledata, headings= accountableheaders, # DEFINE TABLE
                            auto_size_columns=True,
                            justification='centre', key='-TABLE-',
                            selected_row_colors='black on #51b4db',
                            enable_click_events=True,
                            enable_events=True,
                            visible_column_map=[True,True,True] # Shows all columns
                            )
    
    layout = [[AccountTable],
              [sg.Button('Manage Account', key='-MANAGEBUTTON-'), sg.Stretch(), sg.Button('Back', key='-BACK-')],
              [sg.Button('Create Account', key='-CREATE-')]
              ] 

    window = sg.Window('Manage Accounts', layout) 

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '-BACK-':
            break
        if event == '-MANAGEBUTTON-' and values['-TABLE-'] != []:
            selectedaccount = values['-TABLE-'][0]
            window.Close()
            ControlAccounts(selectedaccount)
        if event == '-CREATE-':
            CreateAccountPage()

    window.Close()

### Screen to manage account
def ControlAccounts(account):
    CurrentAccount = accounttabledata[account]
    
    layout = [[sg.Text('Username: '), sg.Stretch(), sg.Input(key='-USERNAMEINPUT-', default_text=CurrentAccount[0], size=(18,1))],
              [sg.Text('Password: '), sg.Stretch(), sg.Input(key='-PASSWORDINPUT-', default_text=CurrentAccount[1], size=(18,1))],
              [sg.Text('Prvilege: '), sg.Stretch(), sg.DropDown(values=('User','Technician','Admin'),key='-PRIVILEGE-', size= (9,1), default_value=CurrentAccount[2])],
              [sg.HSeparator()],
              [sg.Button('Save', key='-SAVE-'),sg.Text('',key='-CONFIRM-'), sg.Stretch(), sg.Button('Back', key='-BACK-')]
              ] 

    window = sg.Window('Manage Account', layout, size=(350,120)) 

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '-BACK-':
            break

        if event == '-SAVE-':
            RowToSave = [values['-USERNAMEINPUT-'], values['-PASSWORDINPUT-'], values['-PRIVILEGE-']]
            with open('accounts.csv', 'w', newline='') as accountsfile3:
                writer = csv.writer(accountsfile3)
                count = 0
                for row in accounttabledata:           # REWRITES CSV, IF CURRENTLY EDITED ACCOUNT = ACCOUNT INDEX IN TABLE, THEN REWRITES NEW DATA TO THIS LINE.   
                    if count == account:
                        writer.writerow(RowToSave)
                    else:
                        writer.writerow(accounttabledata[count])
                    count = count + 1
                window['-CONFIRM-'].update('Saved.')
            
            RefreshAccountTable()
     
    window.Close()
    AccountsTablePage()

RefreshAccountTable()
RefreshTicketTable()
Main()