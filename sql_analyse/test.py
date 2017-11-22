from sql_structure import SqlBlock

d=SqlBlock('select (a(b(c))) (bb(dd(ee)))')
c=SqlBlock(' (a) (b)  bb   all (asfd)  (asfd)maaa')

def initialize_sqls(sql_block):
    sql_block.initialize_sql_block()
    #print  sql_block.inner_sql_strings
    for innersql in sql_block.inner_sql_strings:
        inner_sql_block = SqlBlock(innersql)
        inner_sql_block=initialize_sqls(inner_sql_block)
        sql_block.inner_sql_blocks.append(inner_sql_block)
    return sql_block


#initialize_sqls(d)

print 'a'