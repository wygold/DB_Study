class TableField:
    propertytypes = [
    'name',
    'length',
    'datatype',
    'isindex',
    'isnullable'
    ]
    properties = dict()

    def __init__(self, name):
        None

    def setFieldProperties(self, name, length, datatype, isindex, isnullable):
        self.properties['name']=name
        self.properties['length'] = length
        self.properties['datatype'] = datatype
        self.properties['isindex'] = isindex
        self.properties['isnullable'] = isnullable

    def setFieldProperty(self, propertytype, propertyvalue):
        if propertytype in self.propertytypes:
            self.properties[propertytype] = propertyvalue
            return True
        else:
            return False

    def getTableProperty(self, propertytype, propertyvalue):
        if propertytype in self.propertytypes:
            return self.properties[propertytype]
        else:
            return ''


class Table:

    name = ''
    descritpion =''
    tablefields = dict()

    def __init__(self, name, descritption = ''):
        self.name = name
        if descritption <> '':
            self.descritpion = descritption

    def addtablefield(self, name, length, datatype, is_index, is_nullable):

        if self.tablefields.has_key(name):
            return False
        else:
            tablefield = TableField(name)
            self.tablefields[name]=tablefield.setFieldProperties(name, length, datatype, is_index, is_nullable)

        return True

    def gettablefields(self):
        return self.tablefields




