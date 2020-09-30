from generater import Inspect
from graphviz import Digraph

graph = Digraph('structs', filename='ER.gv',
                node_attr={'shape': 'record'})


def tabulate(arr):
    msg = ''
    for i in range(len(arr)):
        if i is not (len(arr)-1):
            msg = msg + '<f{}>{} |'.format(i, arr[i])
        else:
            msg = msg + '<f{}>{}'.format(i, arr[i])

    return msg


table_data = Inspect('sqlite:///chinook.db')
tables = table_data.get_details()
print(tables)

for table in tables.keys():
    graph_rows = [table] + list(tables[table]['columns'].keys())
    graph.node('{}'.format(table), r'{ %s }' % (tabulate(graph_rows)))

    for column in tables[table]['columns'].keys():
        if 'relationship_to' in list(tables[table]['columns'][column].keys()):
            rel = tables[table]['columns'][column]['relationship_to']
            col_index_host = list(
                tables[table]['columns'].keys()).index(column) + 1

            col_index_target = list(
                tables[rel['table']]['columns'].keys()).index(rel['column']) + 1
            print(col_index_host)
            print(col_index_target)

            graph.edge('{}:f{}'.format(table, col_index_host),
                       '{}:f{}'.format(rel['table'], col_index_target))


graph.view()
