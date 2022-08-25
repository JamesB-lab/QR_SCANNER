from math import prod
import pandas as pd
from io import StringIO
from datetime import datetime
from sqlalchemy import create_engine




string = "2017-07-12,395R1,ZL70642MJX"
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


print(df)

#SQL Connection Windows Authentication#

Server = 'UKC-VM-SQL01'
Database = 'Stencil'
Driver = 'ODBC Driver 17 for SQL Server'
Database_con = f'mssql://@{Server}/{Database}?driver={Driver}'

engine = create_engine(Database_con)
con = engine.connect()

df.to_sql('StencilUsage', con, if_exists='append', index = False)

print('Program complete')