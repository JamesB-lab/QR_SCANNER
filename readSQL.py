from sqlite3 import InterfaceError
import keyboard
from threading import Timer
from datetime import datetime
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import sqlalchemy




def mssql_engine(Server = 'UKC-VM-SQL01',
Database = 'Stencil',
Driver = 'ODBC Driver 17 for SQL Server',):
    engine = create_engine(Database_con)
    return engine


#SQL Connection Windows Authentication#

Server = 'UKC-VM-SQL01'
Database = 'Stencil'
Driver = 'ODBC Driver 17 for SQL Server'
Database_con = f'mssql://@{Server}/{Database}?driver={Driver}'

engine = create_engine(Database_con)
con = engine.connect()

##############

serial_Number = '396R1'

query = sqlalchemy.sql.text('SELECT SerialNumber, COUNT(*) FROM [Stencil].[dbo].[StencilUsage] WHERE SerialNumber = :sn GROUP BY SerialNumber ORDER BY SerialNumber')
# query = f'SELECT SerialNumber, COUNT(*) FROM [Stencil].[dbo].[StencilUsage] GROUP BY SerialNumber ORDER BY SerialNumber'
df = pd.read_sql(query, mssql_engine())

result = con.execute(query, {"sn": serial_Number})
print(result.all())

# if df.loc[df.index[0], 'SerialNumber'] == serial_Number:
#     print(f'Stencil Usage Count = {df.loc[df.index[0], df.loc[df.column[2]]]}')
# else:
#     print('you made an error in your code')

# print(df)

# print(df.loc[df.index[0], 'SerialNumber'])