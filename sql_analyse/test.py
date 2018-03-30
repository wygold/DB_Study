import re

from sql_structure import SqlBlock




#d=SqlBlock('select (a(b(c))) (bb(dd(ee)))')
d=SqlBlock('select aaa from AAA_DBF T1,  AFS T2,  adf T3 where T1.A=T2.B and T2.a=(select t2.3 from a where m=b) and t3.4=t44.1')
# c=SqlBlock(' (a) (b)  bb   all (asfd)  (asfd)maaa')
# e = SqlBlock ('   (            select M_RPO_DMSETUP_TABLE_REF , count(*) "COLUMNS_COUNT" from RPO_DMSETUP_COLUMN_DBF          group by M_RPO_DMSETUP_TABLE_REF) B ')

print d.outer_tables

#d.parse_table_name_and_alias()




