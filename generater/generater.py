"""Main module."""

from sqlalchemy import create_engine
from sqlalchemy.engine import reflection


# Class that uses the Inspector class to inspect the .db file


class Inspect:
    engine = None
    inspector = None

    def __init__(self, path_to_db_file):
        self.engine = create_engine(path_to_db_file)
        self.inspector = reflection.Inspector.from_engine(self.engine)

    # Function to return details about columns, primary and foreign-keys of
    # all tables in the .db file
    def get_details(self):
        tables_list = self.inspector.get_table_names()
        result = {}
        for table in tables_list:
            result[table] = self.get_columns_for_table(table)
        return result

    # Function that fetches the details about the columns of a particular table
    def get_columns_for_table(self, table):
        response = {
            'name': table
        }
        columns = self.inspector.get_columns(table)
        fks = self.inspector.get_foreign_keys(table)
        all_columns = {}
        for column in columns:
            column_name = column['name']
            res = {
                'name': column_name,
                'data_type': column['type'],
                'is_primary_key': bool(column['primary_key'])
            }
            res = self.fetch_fks(table, res, fks)
            all_columns[column_name] = res
        response['columns'] = all_columns
        return response

    # Function that takes in details about a column and adds the relationship
    # details if column is a foreign-key
    # If column is not a foreign-key, it adds 'is_foreign_key':False to the
    # details about the column
    def fetch_fks(self, table, column_dict, fks):
        column_name = column_dict['name']
        if len(fks) == 0:
            column_dict['is_foreign_key'] = False
            return column_dict
        for key in fks:
            if column_name == key['constrained_columns'][0]:
                column_dict['is_foreign_key'] = True
                column_dict['relationship_to'] = {
                    'table': key['referred_table'],
                    'column': key['referred_columns'][0]
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
"""

"""
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
         }
      }
   }
}
"""
