select
T2.M_LABEL as LABEL,
T2.M_REQUEST
--utl_raw.cast_to_varchar2(dbms_lob.substr(T2.M_REQUEST, 2000))
from ACT_REQPROC_DBF T2