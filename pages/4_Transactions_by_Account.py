import streamlit as st
import pandas as pd
import sqlite3
from utils.get_account_dbs import get_account_dataframe

ACCOUNTS_PATH = 'accounts/'

st.set_page_config(page_title="Check your accounts transactions")

st.markdown("# Select a filter to apply to the data")


accounts = get_account_dataframe()

select_account = st.selectbox('Select an Account:', accounts['Account_Name'].tolist())

conn = sqlite3.connect(ACCOUNTS_PATH+select_account)
sql = 'select * from mytable'
data = pd.read_sql(con=conn, sql=sql)

st.write(f'These are you transactions for account {select_account}', data)
# cursor = conn.cursor()
# cursor.execute('select ')


