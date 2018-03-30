from table import Table

class TableRelationship:
    table1 = Table()
    table2 = Table()
    relation = ()

    def __init__(self, table1, table2):
        self.table1 = table1
        self.table2 = table2


    def add_relationship(self, table1, table2, field1, field2):
        pass


