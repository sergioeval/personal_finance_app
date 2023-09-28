import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
import sqlite3
from utils.db_connector import Db_Connector

db_connector = Db_Connector()

st.set_page_config(page_title="Create New Records")

st.markdown("# Create new records here")


accounts_dbs_list = db_connector.get_unique_account_names_list()
#print(accounts_dbs_list)

categories_list = db_connector.get_unique_categories_list()

SQL_TEMPLATES_PATH = 'sql_templates/'
ACCOUNTS_PATH = 'accounts/'

with open(SQL_TEMPLATES_PATH+'new_record_template.sql', mode='r') as f:
    sql_new_record_template = f.read()

with open(SQL_TEMPLATES_PATH+'new_transfer_from_temp.sql', mode='r') as f:
    sql_new_transfer_from_template = f.read()

with open(SQL_TEMPLATES_PATH+'new_transfer_to_temp.sql', mode='r') as f:
    sql_new_transfer_to_template = f.read()

# print(sql_new_accounts)


with st.form("record_creation", clear_on_submit=True):
    st.write('Create here your new record\n')
    account_selected = st.selectbox('First Select the account: ', accounts_dbs_list)

    st.write('Provide the data \n')
    mov_date = st.date_input('Select the Transaction Date')

    mov_category = st.selectbox('Transaction Category', categories_list)
    mov_type = st.selectbox('Transaction Type', db_connector.get_mov_types_list())
    account_to_transfer = st.selectbox('To what account is this transfer for: ', accounts_dbs_list)
    mov_amount = st.number_input('Enter Amount')

    submitted = st.form_submit_button("Submit", )

    if submitted:
        if (mov_amount != 0) & (mov_type != 'TRANSFERS'):
            sql_new_record_template = sql_new_record_template.format(mov_date, mov_category, mov_type, mov_amount)
            # print(sql_new_record_template)
            db_connector.modify_db_sql(sql=sql_new_record_template, db_name=account_selected)
        
        if (mov_amount != 0) & (mov_type == 'TRANSFERS'):
            # add record to account FROM 
            sql_transfer_from = sql_new_transfer_from_template.format(mov_date, 
                                                                      mov_category, 
                                                                      mov_type, 
                                                                      -mov_amount, 
                                                                      account_to_transfer)
            db_connector.modify_db_sql(sql=sql_transfer_from, db_name=account_selected)
        
            # add record to account TO 
            sql_transfer_to = sql_new_transfer_to_template.format(mov_date, 
                                                                  mov_category, 
                                                                  mov_type, 
                                                                  mov_amount,
                                                                  account_selected)
            db_connector.modify_db_sql(sql=sql_transfer_to, db_name=account_to_transfer)
