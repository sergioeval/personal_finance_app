import sqlite3
import glob
import pandas as pd

class Db_Connector:
    '''
    for database connectivity to sqlite3
    Actions: 
        get Df of all db names 
        get db names in a list
        get df from an sql and a db name
        run a query in db 
    '''
    def __init__(self):
        self.ACCOUNTS_PATH = 'accounts/'
        self.CATEGORIES_PATH = 'categories/'
        self.categories_account_name = 'categories.db'

    def get_all_account_names_df(self):
        account_list = glob.glob(self.ACCOUNTS_PATH+'*.db', recursive=True)
        account_list = [acc.split('/')[1] for acc in account_list]

        accounts_data = []
        for acc in account_list:
            temp = {
                'Account_Name': acc
            }
            accounts_data.append(temp)

        acc_df = pd.DataFrame(accounts_data)
        return acc_df

    def get_db_names_list(self):
        accounts_df = self.get_all_account_names_df()
        accounts_list = accounts_df['Account_Name'].tolist()
        return accounts_list

    def _connect_to_db(self, db_name='', is_category_db=False):
        '''Connect to db '''
        if is_category_db:
            self.connection = sqlite3.connect(self.CATEGORIES_PATH+self.categories_account_name)

        if is_category_db == False:
            self.connection = sqlite3.connect(self.ACCOUNTS_PATH+db_name)

        self.cur = self.connection.cursor()

    def _close_connection(self):
        self.connection.close()

    def sql_to_df(self, sql, db_name='', is_category_db=False):
        self._connect_to_db(db_name, is_category_db)
        data = pd.read_sql(sql=sql, con=self.connection)
        self._close_connection()
        return data

    def modify_db_sql(self, sql, db_name='', is_category_db=False):
        self._connect_to_db(db_name, is_category_db)
        self.cur.execute(sql)
        self.connection.commit()
        self._close_connection()

    def update_record_accounts(self, db_name, sql, new_value, record_id):
        self._connect_to_db(db_name=db_name)
        self.cur.execute(sql, (new_value, record_id))
        self.connection.commit()
        self._close_connection()

    def get_unique_categories_list(self):
        self._connect_to_db(is_category_db=True)
        categories_df = pd.read_sql(sql='select category from mytable', 
                                    con=self.connection)
        categories_list = categories_df['category'].tolist()
        self._close_connection()
        return categories_list

    def get_unique_account_names_list(self):
        accounts_df = self.get_all_account_names_df()
        accounts_list = accounts_df['Account_Name'].tolist()
        return accounts_list

    def get_mov_types_list(self):
        return ['INCOME', 'EXPENSES', 'TRANSFERS']

    def get_all_data_from_all_accounts(self):
        '''
        To get all the data from all accounts into a single dataframe 
        '''
        accounts_list = self.get_unique_account_names_list()
        all_data = pd.DataFrame()

        for acc in accounts_list:
            temp = self.sql_to_df(sql='select * from mytable', 
                                  db_name=acc)
            temp['account'] = acc
            all_data = pd.concat([all_data, temp], ignore_index=True)

        all_data['mov_date'] = pd.to_datetime(all_data['mov_date'])
        all_data['MOV_YEAR'] = all_data['mov_date'].dt.year
        all_data['MOV_MONTH'] = all_data['mov_date'].dt.month
        all_data.sort_values(by='mov_date', ascending=True, inplace=True)

        return all_data

    def get_data_from_account_and_month(self, db_name, month_number):
        data = self.sql_to_df(sql='select * from mytable',
                              db_name=db_name)
        data['account'] = db_name
        data['mov_date'] = pd.to_datetime(data['mov_date'])
        data['MOV_YEAR'] = data['mov_date'].dt.year
        data['MOV_MONTH'] = data['mov_date'].dt.month

        data = data[(data['MOV_MONTH'] == month_number)]
        return data







