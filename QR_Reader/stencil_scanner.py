import keyboard # for keylogs
from threading import Timer
from datetime import datetime
from math import prod
import pandas as pd
from io import StringIO
from datetime import datetime
from sqlalchemy import create_engine


SEND_REPORT_EVERY = 3 # in seconds


class Keylogger:
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
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "spac2017-07-12,395R1,ZL70642MJXe"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
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
        # finally, add the key name to our global `self.log` variable
        name = name.upper()
        self.log += name
        

   
    
    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

        if len(self.filename) != 58:
            print('ERROR LOGGING TO SQL, PLEASE TRY AGAIN')



    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "file":
                self.report_to_file()
                # if you don't want to print in the console, comment below line
                print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        
        ###log to SQL###

        if self.log != "" and len(self.log) ==58:
            self.log_sql()
            
                


        ###clear log###
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def log_sql(self):
        
        string = self.log
        stringSplit = string.split(",")

        printerID = 'SP2'
        dateofmanufacture = stringSplit[0]
        serialNumber = stringSplit[1]
        prodFam = stringSplit[2]
        currentDate = datetime.now()
        manuSN = stringSplit[4]
        material = stringSplit[3]
        thickness = stringSplit[5]

        testData = StringIO(string)

        dict = {'PrinterID': printerID, 'DateofManufacture': dateofmanufacture, 'SerialNumber': serialNumber, 'ProductFamily': prodFam, 'CurrentDate': currentDate, 'ManufacturerSN': manuSN, 'Material': material, 'Thickness': thickness}

        df = pd.DataFrame.from_dict(dict, orient='index')
        df = df.transpose()

        #SQL Connection Windows Authentication#

        Server = 'UKC-VM-SQL01'
        Database = 'Stencil'
        Driver = 'ODBC Driver 17 for SQL Server'
        Database_con = f'mssql://@{Server}/{Database}?driver={Driver}'

        engine = create_engine(Database_con)
        con = engine.connect()

        
        df.to_sql('StencilUsage', con, if_exists='append', index = False)
        print('LOGGED TO SQL')
        

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
        print(f"{datetime.now()} - Started QR Scanner")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

    
if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()