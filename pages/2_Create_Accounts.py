import streamlit as st
import time
# import numpy as np
import sqlite3
import os
import glob
import pandas as pd
from utils.get_account_dbs import get_account_dataframe

ACCOUNTS_PATH = 'accounts/'
SQL_TEMPLATES_PATH = 'sql_templates/'

with open(SQL_TEMPLATES_PATH+'new_accounts.sql', mode='r') as f:
    sql_new_accounts = f.read()
# print(sql_new_accounts)

st.set_page_config(page_title="Create Accounts")

st.markdown("# Create your accounts here")
# paragraph 
st.write('''
In this page you will be able to create you personal debit or credit accounts. 
''')

# form 
with st.form("new_account_form", clear_on_submit=True):
   st.write("Provide the Account Information:")
   acccount_name = st.text_input('Account Name')
   account_type = st.selectbox('Select an account Type', ['Credit', 'Debit'])

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit", )

   if submitted:
        ACCOUNT_NAME = acccount_name.upper().replace(' ', '_')
        ACCOUNT_TYPE = account_type.upper()
        FINAL_NAME = ACCOUNTS_PATH+ACCOUNT_NAME+'_'+ACCOUNT_TYPE

        if os.path.exists(FINAL_NAME+'.db'):
            st.write(f'The account with the name {FINAL_NAME} already exists.')
        
        if (not os.path.exists(FINAL_NAME+'.db')) & (acccount_name != ''):
            conn = sqlite3.connect(FINAL_NAME+'.db')
            # create table in db 
            cursor = conn.cursor()
            # Create a table in the database
            cursor.execute(sql_new_accounts)
            conn.close()
            st.write(f'The Account {FINAL_NAME} was created sucessfully') 

        if (acccount_name==''):
            st.write('YOU NEED TO PROVIDE AN ACCOUNT NAME')



acc_df = get_account_dataframe()


st.write(f'Your created accounts: ', acc_df)
