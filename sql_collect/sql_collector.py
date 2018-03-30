__author__ = 'ywang'

import os
from os import listdir
from os.path import isfile, join
from db_utility import db_utility
from io_utility import io_utility

# 1 collect SQL from datamart extraction
def collect_dm_sql(db_source_file):
    db_util = db_utility()
    io_util = io_utility()
    connectionString = db_util.load_dbsourcefile(db_source_file)
    db_type = db_util.db_type
    DbDatabaseOrSchemaName = db_util.DbDatabaseOrSchemaName
    # SQL query to get REP table SQL code
    sqlfile = open('SQL_Queries\\'+db_type+'\\query_dm_extraction_sql.sql', 'r+')
    sqlString = ''
    for line in sqlfile:
        sqlString = sqlString + line

    # prepare sql paramaters, the paramaters are defined according to MX format @:paramater_name:N/D/C
    sql_paramters = dict()

    # execute SQL
    result = db_util.execute_sql(sqlString, sql_paramters, connectionString)
    # dump file
    for extraction in result:
        filename= extraction[0].strip()+".sql"
        content = extraction[1]
        io_util.write_txt('Client_SQLs\\'+DbDatabaseOrSchemaName+'\\DM_Extraction', filename,content)

# 2 collect SQL from trace file
def collect_trace_sql():
    pass

def find_trace_files():
    pass

def sql_collector():
    # read db source file
    db_source_dir = 'dbsource_files'
    db_source_files = [f for f in listdir(db_source_dir) if isfile(join(db_source_dir, f))]

    for db_source_file in db_source_files:
        collect_dm_sql(db_source_dir+'\\' + db_source_file)

