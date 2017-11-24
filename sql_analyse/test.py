from sql_structure import SqlBlock

#d=SqlBlock('select (a(b(c))) (bb(dd(ee)))')
d=SqlBlock('select aaa from AAA_DBF T1,  AFS T2, (select * from A_DBF t3) t4, adf T3')
# c=SqlBlock(' (a) (b)  bb   all (asfd)  (asfd)maaa')
# e = SqlBlock ('   (            select M_RPO_DMSETUP_TABLE_REF , count(*) "COLUMNS_COUNT" from RPO_DMSETUP_COLUMN_DBF          group by M_RPO_DMSETUP_TABLE_REF) B ')


def initialize_sqls(sql_block):
    sql_block.initialize_sql_block()
    #print  sql_block.inner_sql_strings
    for innersql in sql_block.inner_sql_strings:
        inner_sql_block = SqlBlock(innersql)
        inner_sql_block=initialize_sqls(inner_sql_block)
        sql_block.inner_sql_blocks.append(inner_sql_block)
    return sql_block


#d.parse_table_name_and_alias()

print 'select aaa from AAA_DBF T1, AFS T2'.replace(',',' , ')