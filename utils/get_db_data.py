
import sqlite3
import pandas as pd
from utils.get_account_dbs import get_account_dataframe

CATEGORIES_PATH = 'categories/'
ACCOUNTS_PATH = 'accounts/'

def get_all_data_from_all_accounts():
    '''
    To get all the data from all accounts into a single dataframe 
    '''
    accounts = get_account_dataframe()
    accounts_list = accounts['Account_Name'].tolist()

    all_data = pd.DataFrame()

    for acc in accounts_list:
        conn = sqlite3.connect(ACCOUNTS_PATH+acc)
        temp = pd.read_sql(con=conn, sql='select * from mytable')
        temp['account'] = acc
        all_data = pd.concat([all_data, temp], ignore_index=True)

    all_data['mov_date'] = pd.to_datetime(all_data['mov_date'])
    all_data['MOV_YEAR'] = all_data['mov_date'].dt.year
    all_data['MOV_MONTH'] = all_data['mov_date'].dt.month
    
    return all_data



def get_categories():
    '''
    Get categories from database and return list of categories. 
    '''
    conn = sqlite3.connect(CATEGORIES_PATH+'categories.db')
    # sql to get all categories 
    sql = '''select category from mytable'''
    data = pd.read_sql(con=conn, sql=sql)
    
    category_list = data['category'].tolist()
    return data, category_list

def get_types():
    '''
    get types from string 
    '''
    return ['INCOME', 'EXPENSES', 'TRANSFERS']