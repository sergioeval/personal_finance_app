from streamlit_calendar import calendar
import streamlit as st
from utils.db_connector import Db_Connector
from utils.general_utils import get_number_days_to_transactions
import datetime


connector = Db_Connector()

all_accounts_data = connector.get_all_data_from_all_accounts()

del all_accounts_data['transfer_from']
del all_accounts_data['transfer_to']
del all_accounts_data['id']

cur_date = datetime.datetime.now()

# filter data >= cur_date
all_accounts_data = all_accounts_data[
    all_accounts_data['mov_date'] >= cur_date
]

all_accounts_data['DAYS_TO_TRANSACTION'] = all_accounts_data.apply(
    lambda row: get_number_days_to_transactions(mov_date=row['mov_date']), 
    axis=1
)
print(all_accounts_data)


st.write('# Here you can see the Future transactions')

st.write('All Future Transactions', all_accounts_data)
