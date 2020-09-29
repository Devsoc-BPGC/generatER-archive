from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.engine import reflection
from sqlalchemy import create_engine, MetaData, Table,inspect
from sqlalchemy.orm.interfaces import ONETOMANY, MANYTOMANY, MANYTOONE
from sqlalchemy_utils import get_mapper, get_class_by_table
from sqlalchemy.ext.automap import automap_base


Base = declarative_base()
path='sqlite:///chinook.db'   ##change this path according to file location of db
engine = create_engine(path)
meta = MetaData(engine)
insp = reflection.Inspector.from_engine(engine)
table_names = insp.get_table_names()

count=int(1)
for_key={   }
columns={}
for table_loop in table_names: #loops through all the tables
    primary_keys=[]
    print(str(count)+". "+table_loop)
    count+=1
    columns[table_loop]=insp.get_columns(table_loop)    #to store coulumns of each table
    for_key[table_loop]=insp.get_foreign_keys(table_loop)       #to store a list of all foreign keys of table
    print("- Columns :   ")
    for column in columns[table_loop]:
        print("  " + column['name'])
        if column['primary_key']:
            primary_keys.append(column['name'])    #primary keys
    for i in primary_keys:
        print("- Primary Key     "+i)               #prints primary keys
    for key in for_key[table_loop]:
        print("- ForeignKey : "+key['referred_table']+ "."+key['constrained_columns'][0])       #prints foreign keys

metadata = MetaData(bind=engine,  reflect=True)

Base = automap_base(metadata=metadata)
Base.prepare()

for t in columns:
    table = Table(t, metadata)
    cl = get_class_by_table(Base, table)
    try:
        for relation in cl.__mapper__.relationships:
            print(relation)                             #type of reltaion (Many to one or one to many)
            print(relation.direction)                   #direction of relation 
    except:
        pass
