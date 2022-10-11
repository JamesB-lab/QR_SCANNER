from sqlite3 import InterfaceError
import keyboard
from threading import Timer
from datetime import datetime
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine


SEND_REPORT_EVERY = 3 # in seconds


class Scanner:
    def __init__(self, interval, report_method="file"):
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all 
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        
        if len(name) > 1:
            #Not a character, special key (e.g ctrl, alt, etc.)
            #Uppercase with []
            if name == "space":
                name = " "
            elif name == "enter":
                name = ""
            elif name == "decimal":
                name = "."
            elif name == "shift":
                name = ""
            elif name == name.lower():
                name = name.upper()
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        #Add the key name to our global `self.log` variable
        name = name.upper()
        self.log += name

    
        

   
    
    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"Stencil_QR_Scanner-{start_dt_str}_{end_dt_str}"


    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current scanner logs in the `self.log` variable"""
        # open the file in write mode (create it)
        
        with open(f"{self.filename}.txt", "w") as f:
            # write the scan logs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
    

    def report(self):
        """
        This function gets called every `self.interval`
        It  sends scanner logs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "file":
                #self.report_to_file()
                # if you don't want to print in the console, comment below line
                print(f"[{self.filename}] - Waiting for Input...")
            self.start_dt = datetime.now()
        
        ###log to SQL###

        if self.log != "" and len(self.log) ==59:
            self.log_sql()  

        ###clear log###
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()
    
    def log_sql(self):
        try:
            scannedString = self.log
            print(scannedString)
            stringSplit = scannedString.split(",")

            #print(len(string))

            #2017-07-12,395,R1,ZL70642MJX,STAINLESS_STEEL,GB031958,0.005

            printerID = 'SP3'
            dateofmanufacture = stringSplit[0]
            stencilNumber = stringSplit[1]
            revision = stringSplit[2]
            prodFam = stringSplit[3]
            currentDate = datetime.now()
            manuSN = stringSplit[5]
            material = stringSplit[4]
            thickness = stringSplit[6]


            mydict = {'PrinterID': printerID, 'DateofManufacture': dateofmanufacture, 'StencilNumber': stencilNumber, 'Revision': revision, 'ProductFamily': prodFam, 'CurrentDate': currentDate, 'ManufacturerSN': manuSN, 'Material': material, 'Thickness': thickness}

            df = pd.DataFrame.from_dict(mydict, orient='index')
            df = df.transpose()

            #SQL Connection Windows Authentication#

            Server = 'UKC-VM-SQL01'
            Database = 'Stencil'
            Driver = 'ODBC Driver 17 for SQL Server'
            Database_con = f'mssql://@{Server}/{Database}?driver={Driver}'

            engine = create_engine(Database_con)
            con = engine.connect()


            df.to_sql('StencilUsage', con, if_exists='append', index = False)
            print(f'LOGGED TO SQL at {datetime.now()}')



        except Exception:
            print('ERROR CONNECTING TO SQL')
        

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the scanner
        keyboard.on_release(callback=self.callback)
        # start reporting the scanner input
        self.report()
        print(f"{datetime.now()} - Started QR Scanner for SP3")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

    
if __name__ == "__main__":
    scanner = Scanner(interval=SEND_REPORT_EVERY, report_method="file")
    scanner.start()