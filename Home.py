import streamlit as st
import pandas as pd
import sqlite3
from utils.general_utils import change_symbol, format_currency
import time 
from utils.boxApiJson import BoxApiJson
import glob
import datetime
from utils.db_connector import Db_Connector


BOX_CREDS = 'secrets/'
box_api = BoxApiJson(jsonPath=BOX_CREDS+'BoxCredentials.json')
box_accounts_folder_id = '227810718878'
box_categories_folder_id = '227810963459'
ACCOUNTS_PATH = 'accounts/'

db =  Db_Connector()

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)


st.write("# Welcome to this Minimal version of Open Personal Finance App 👋")

st.markdown(
    """
    In this App you will be able to control your personal finances all in one place.

    **👈 Select one of the options in the left menu** 

    Start by creating new accounts and categories.
"""
)



# ------------- MAIN CONTENT STARTS HERE --------------------
# Create columns for tables 
col1, col2 = st.columns(2)

# get current date 
current_date = datetime.datetime.now() 

#current_date = current_date.strftime('%Y-%m-%d')

# get databases and filter only to current date 
#all_data = get_all_data_from_all_accounts()
all_data =db.get_all_data_from_all_accounts()
all_data = all_data[(all_data['mov_date'] <= current_date)]



all_data['amount'] = all_data.apply(lambda row: change_symbol(mov_type=row['mov_type'], val=row['amount']), axis=1)

#pivot table 
pivot_table = all_data.copy()
pivot_table = pd.pivot_table(pivot_table, values='amount', index='account', aggfunc='sum', margins=True)
pivot_table['amount'] = pivot_table['amount'].apply(format_currency)

# data only debit for col2 
debits_data = all_data.copy()
debits_data = debits_data[debits_data['account'].str.contains('DEBIT')]
debits_data = pd.pivot_table(debits_data, values='amount', index='account', aggfunc='sum', margins=True)
debits_data['amount'] = debits_data['amount'].apply(format_currency)
# print(debits_data)

with col1:
    #st.write('All Accounts Totals: ', pivot_table)
    st.write('### Totals All Accounts')
    st.dataframe(data=pivot_table, height=450)

with col2:
    st.write('### Debit Accounts')
    st.dataframe(data=debits_data, height=300)

# ------------------ MAIN CONTENT ENDS HERE -----------------------
