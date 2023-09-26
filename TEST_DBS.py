from utils.db_connector import Db_Connector



db_conn = Db_Connector()


account_list = db_conn.get_db_names_list()
print(account_list)

alter1 = '''
ALTER TABLE mytable
ADD COLUMN "transfer_from" TEXT
'''
alter2 = '''
ALTER TABLE mytable
ADD COLUMN "transfer_to" TEXT
'''

for db in account_list:
    try:
        #db_conn.modify_db_sql(sql=alter1, db_name=db)
    except:
        pass

    try:
        #db_conn.modify_db_sql(sql=alter2, db_name=db)
    except:
        pass

    print(#db_conn.sql_to_df(sql='select * from mytable', db_name=db))


