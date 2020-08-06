from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import reflection
from sqlalchemy.inspection import inspect



Base = declarative_base()
path=input("Enter path here: ")
engine = create_engine(path)
meta = MetaData(engine)
insp = reflection.Inspector.from_engine(engine)
table_names = insp.get_table_names()
print("Tables present in the table are: ")

count=int(1)
for_key={   }
columns={}
for table_loop in table_names:
    print(str(count)+". "+table_loop)
    count+=1
    columns[table_loop]=insp.get_columns(table_loop)
    for_key[table_loop]=insp.get_foreign_keys(table_loop)
    for key in for_key[table_loop]:
        print("- ForeignKey : "+key['referred_table']+ "."+key['constrained_columns'][0])
#print(columns)
