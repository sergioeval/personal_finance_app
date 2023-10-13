import streamlit as st
import pandas as pd
from urllib.error import URLError
import sqlite3
from utils.db_connector import Db_Connector

db_connector = Db_Connector()

st.set_page_config(page_title="Create New Records")

st.markdown("# Create new records here")


SQL_TEMPLATES_PATH = 'sql_templates/'

with open(SQL_TEMPLATES_PATH+'new_record_template.sql', mode='r') as f:
    sql_new_record_template = f.read()


with st.form("record_creation", clear_on_submit=True):

    st.write('Provide the data \n')
    mov_date = st.date_input('Select the Transaction Date')
    mov_type = st.selectbox('Transaction Type', ['CREDIT_PAYMENT', 'INCOME'])
    comments = st.text_input('Comments')
    amount = st.number_input('Enter Amount')

    submitted = st.form_submit_button("Submit", )

    if submitted:
        sql_new_record_template = sql_new_record_template.format(mov_date, mov_type, amount, comments)
        # print(sql_new_record_template)
        db_connector.run_query_on_db(sql=sql_new_record_template)
    
