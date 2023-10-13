import streamlit as st
import pandas as pd
from urllib.error import URLError
import sqlite3
from utils.db_connector import Db_Connector

db_connector = Db_Connector()

st.set_page_config(page_title="Create New Date Group")

st.markdown("# Create new date groups here")


SQL_TEMPLATES_PATH = 'sql_templates/'

with open(SQL_TEMPLATES_PATH+'new_record_date_groups.sql', mode='r') as f:
    sql_new_record_template = f.read()


with st.form("record_creation", clear_on_submit=True):

    st.write('Provide the data \n')
    start_date = st.date_input('Enter here the START DATE')
    end_date = st.date_input('Enter here the END DATE')
    label = st.text_input('Enter the name for this group')

    submitted = st.form_submit_button("Submit", )

    if submitted:
        sql_new_record_template = sql_new_record_template.format(start_date, end_date, label.strip().upper())
        # print(sql_new_record_template)
        db_connector.run_query_on_db(sql=sql_new_record_template)
    
