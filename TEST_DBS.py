from utils.db_connector import Db_Connector



db_conn = Db_Connector()


account_list = db_conn.get_db_names_list()
print(account_list)

alter1 = '''
ALTER TABLE mytable
ADD COLUMN "comments" TEXT
'''

for db in account_list:
    db_conn.modify_db_sql(sql=alter1, db_name=db)



