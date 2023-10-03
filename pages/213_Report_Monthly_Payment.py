import streamlit as st
import pandas as pd
from utils.general_utils import change_symbol, format_currency
import time 
import glob
import datetime
from utils.db_connector import Db_Connector


# create connector  
connector = Db_Connector()

# get all data 
payments_data = connector.get_all_data_from_all_accounts_payments_only()
income_data = connector.get_all_data_from_all_accounts_incomes_only()

all_data = pd.concat([payments_data, income_data], ignore_index=True)
print(all_data)

with st.form('get_dates', clear_on_submit=True):
    st.write('### Provide the in between dates to calculate:')


    # submit 
    submitted = st.form_submit_button('Submit',)

    if submitted:
        pass 





