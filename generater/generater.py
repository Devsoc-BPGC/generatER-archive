"""Main module."""

from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from sqlalchemy import create_engine, MetaData, Table,inspect
from sqlalchemy.orm.interfaces import ONETOMANY, MANYTOMANY, MANYTOONE
from sqlalchemy_utils import get_mapper, get_class_by_table
from sqlalchemy.ext.automap import automap_base

# Class that uses the Inspector class to inspect the .db file


class Inspect:
    engine = None
    inspector = None

    def __init__(self, path_to_db_file):
        self.engine = create_engine(path_to_db_file)
        self.inspector = reflection.Inspector.from_engine(self.engine)

    def get_details(self):
        """
        Function to return details about columns, primary and foreign-keys of
        all tables in the .db file
        """
        tables_list = self.inspector.get_table_names()
        result = {}
        for table in tables_list:
            result[table] = self.get_columns_for_table(table)
        
        return result

    def get_columns_for_table(self, table):
        """
        Function that fetches the details about the columns of a particular
        table
        """
        metadata = MetaData(bind=self.engine,  reflect=True)
        Base = automap_base(metadata=metadata)
        Base.prepare()
        relations=Table(table,metadata)
        cl = get_class_by_table(Base, relations)

        table_props = {}
        columns = self.inspector.get_columns(table)
        fks = self.inspector.get_foreign_keys(table)
        all_columns = {}
        for column in columns:
            col_name = column['name']
            column_props = {
                'data_type': column['type'],
                'is_primary_key': bool(column['primary_key'])
            }
            column_props = self.fetch_fks(table, column_props, fks, col_name)
            all_columns[col_name] = column_props

        """
        This part fetches the type of relations
        ____ISSUE: Not able to find out any relation other that ManyToOne and OneToMany
        """
        try:
            for relation in cl.__mapper__.relationships:
                column_props['relationship_info'] = {
                    'type': str(relation.direction)
                }

        except:  #code not working for relations other than manytoone and onetomany
            pass
        
        table_props['columns'] = all_columns
        return table_props

    def fetch_fks(self, table, column_dict, fks, column_name):
        """
        Function that takes in details about a column and adds the relationship
        details if column is a foreign-key
        If column is not a foreign-key, it adds 'is_foreign_key':False to the
        details about the column
        """

        if len(fks) == 0:
            column_dict['is_foreign_key'] = False
            return column_dict
        for foreign_key in fks:
            if column_name == foreign_key['constrained_columns'][0]:

                column_dict['is_foreign_key'] = True
                column_dict['relationship_to'] = {
                    'table': foreign_key['referred_table'],
                    'column': foreign_key['referred_columns'][0]
                }
            else:
                column_dict['is_foreign_key'] = False
        return column_dict

"""
In case you want to find out the format of the dictionary being returned or
want to test out the code, download the chinook.db file from the sqlite
official website in the ./generater directory and
run the following code

import pprint
pp = pprint.PrettyPrinter()
pp.pprint(Inspect('sqlite:///chinook.db').get_details())

Format of the dictionary returned by getDetails() function:

{
   <table-name>:{
      "name":<name of the table: string>
      "columns":{
         <column-name>:{
            "name":<name of the column: string>,
            "data_type":<SQL type of the column string>,
            "is_primary_key": bool,
            "is_foreign_key": bool

            if "is_foreign_key":True, it includes another field -

            "relationship_to":{
               "table":<name of the table to which the foreign-key points>,
               "column":<name of the column to which the foreign-key points>
            }
            "relationship_info":{
                'related to': <>,
                'type': <manytoone or onetomany relation>
            }
         }
      }
   }
}
"""
