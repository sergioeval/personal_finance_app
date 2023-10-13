import streamlit as st
import pandas as pd
import sqlite3
from utils.general_utils import change_symbol, format_currency
import time 
from utils.boxApiJson import BoxApiJson
import glob
import datetime
from utils.db_connector import Db_Connector

# session state
if 'start_date' not in st.session_state:
    st.session_state.start_date = None

if 'end_date' not in st.session_state:
    st.session_state.end_date = None


BOX_CREDS = 'secrets/'
box_api = BoxApiJson(jsonPath=BOX_CREDS+'BoxCredentials.json')
box_accounts_folder_id = '227810718878'
box_categories_folder_id = '227810963459'

db =  Db_Connector()

all_data = db.sql_to_df(sql='select * from transactions')
all_data['amount'] = all_data.apply(lambda row: change_symbol(mov_type=row['mov_type'], val=row['amount']), axis=1)
all_data['mov_date'] = pd.to_datetime(all_data['mov_date'])
print(type(all_data['mov_date'][0]))

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)


st.write("## Welcome to this Minimal version of Open Personal Finance App 👋")

st.markdown(
    """
    In this App you will be able to control your personal finances all in one place.

    **👈 Select one of the options in the left menu** 

    Start by creating new accounts and categories.
"""
)


with st.form('get_dates', clear_on_submit=True):
    st.write('### Provide the in between dates to calculate:')
    start_date = st.date_input('Start Date:')
    end_date = st.date_input('End Date:')

    # submit
    submitted = st.form_submit_button('Submit',)

    if submitted:
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date

if st.session_state.start_date and st.session_state.end_date:
    if st.session_state.start_date >= st.session_state.end_date:
        st.warning('# Please provide and End date greater than the Start Date')
    
    if st.session_state.start_date < st.session_state.end_date:
        all_data = all_data[(all_data['mov_date'] >= pd.Timestamp(st.session_state.start_date)) & (
            all_data['mov_date'] <= pd.Timestamp(st.session_state.end_date))]
        all_data.reset_index(inplace=True, drop=True)

        st.write('### These are all Payments and Incomes: ')
        st.dataframe(data=all_data, height=300)

        st.write('### Summary Totals: ',
                 format_currency(all_data['amount'].sum()))


