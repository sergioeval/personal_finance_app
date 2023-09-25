#%%
from utils.get_account_dbs import get_account_dataframe
import sqlite3
import pandas as pd

#%%
accounts_df = get_account_dataframe()
accounts_df.head()

#%% variables 
ACCOUNTS_PATH = 'accounts/'

#%%

conn = sqlite3.connect(ACCOUNTS_PATH+'BBVA_DEBIT.db')

#%%
sql = ''' select * from mytable '''
data = pd.read_sql(con=conn, sql=sql)
data.head()
# %%
