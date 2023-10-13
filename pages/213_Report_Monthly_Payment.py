import streamlit as st
import pandas as pd
from utils.general_utils import change_symbol, format_currency
import time 
import glob
import datetime
from utils.db_connector import Db_Connector

# session state 
if 'start_date' not in st.session_state:
    st.session_state.start_date = None

if 'end_date' not in st.session_state:
    st.session_state.end_date = None

# create connector  
connector = Db_Connector()

# get all data 
payments_data = connector.get_all_data_from_all_accounts_payments_only()
income_data = connector.get_all_data_from_all_accounts_incomes_only()

all_data = pd.concat([payments_data, income_data], ignore_index=True)

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
        all_data = all_data[(all_data['mov_date'] >= pd.Timestamp(st.session_state.start_date)) & (all_data['mov_date'] <= pd.Timestamp(st.session_state.end_date)) ]
        all_data.reset_index(inplace=True, drop=True)
        del all_data['id']
        
        st.write('### These are all Payments and Incomes: ')
        st.dataframe(data=all_data, height=300)

        st.write('### Summary Totals: ', format_currency(all_data['amount'].sum()))
