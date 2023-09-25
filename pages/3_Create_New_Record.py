import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from utils.get_account_dbs import get_account_dataframe
from utils.get_db_data import get_categories, get_types
import sqlite3

st.set_page_config(page_title="Create New Records")

st.markdown("# Create new records here")


accounts_dbs = get_account_dataframe()
accounts_dbs_list = accounts_dbs['Account_Name'].tolist()

categories_df, categories_list = get_categories()

SQL_TEMPLATES_PATH = 'sql_templates/'
ACCOUNTS_PATH = 'accounts/'

with open(SQL_TEMPLATES_PATH+'new_record_template.sql', mode='r') as f:
    sql_new_record_template = f.read()
# print(sql_new_accounts)


with st.form("record_creation", clear_on_submit=True):
    st.write('Create here your new record\n')
    account_selected = st.selectbox('First Select the account: ', accounts_dbs_list)

    st.write('Provide the data \n')
    mov_date = st.date_input('Select the Transaction Date')

    mov_category = st.selectbox('Transaction Category', categories_list)
    mov_type = st.selectbox('Transaction Type', get_types())
    account_to_transfer = st.selectbox('To what account is this transfer for: ', accounts_dbs_list)
    mov_amonut = st.number_input('Enter Amount')

    submitted = st.form_submit_button("Submit", )

    if submitted:
        

        if (mov_amonut != 0) & (mov_type != 'TRANSFERS'):
            conn = sqlite3.connect(ACCOUNTS_PATH+account_selected)
            cursor = conn.cursor()

            sql_new_record_template = sql_new_record_template.format(mov_date, mov_category, mov_type, mov_amonut)
            # print(sql_new_record_template)
            cursor.execute(sql_new_record_template)
            conn.commit()
            conn.close()
        
        if (mov_amonut != 0) & (mov_type == 'TRANSFERS'):
            conn_from = sqlite3.connect(ACCOUNTS_PATH+account_selected)
            cursor_from = conn.cursor()

            sql_transfer_from = sql_new_record_template.format(mov_date, mov_category, mov_type, -mov_amonut)
            cursor_from.execute(sql_transfer_from)
            conn_from.commit()
            conn_from.close()

            conn_to = sqlite3.connect(ACCOUNTS_PATH+account_to_transfer)
            cursor_to = conn.cursor()
        
            sql_transfer_to = sql_new_record_template.format(mov_date, mov_category, mov_type, mov_amonut)
            cursor_to.execute(sql_transfer_to)
            conn_to.commit()
            conn_to.close()
