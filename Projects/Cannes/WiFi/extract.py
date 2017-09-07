from Code.Projects.Tracking.Tracking3 import read_redshift
from Code.config import get_pwd


def extract():
    raw = read_redshift(get_pwd(), query)

query = "SELECT DISTINCT 'tablename' FROM 'pg_table_def' WHERE 'schemaname' = 'public' ORDER BY 'tablename'"


data = read_redshift(get_pwd(), query)
print data