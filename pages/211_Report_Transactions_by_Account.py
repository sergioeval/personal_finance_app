import streamlit as st
import pandas as pd
import sqlite3
from utils.db_connector import Db_Connector

ACCOUNTS_PATH = 'accounts/'

st.set_page_config(page_title="Check your accounts transactions")

st.markdown("# Select a filter to apply to the data")

db_connector = Db_Connector()
#accounts = get_account_dataframe()
accounts = db_connector.get_all_account_names_df()

select_account = st.selectbox('Select an Account:', accounts['Account_Name'].tolist())

sql = 'select * from mytable'
data = db_connector.sql_to_df(sql=sql, db_name=select_account)
data.sort_values(by='mov_date', inplace=True, ascending=False)

st.write(f'These are you transactions for account {select_account}', data)
# cursor = conn.cursor()
# cursor.execute('select ')


