import streamlit as st
import pandas as pd 
from utils.general_utils import change_symbol, format_currency
import datetime
from utils.db_connector import Db_Connector


st.set_page_config(
    page_title="Future Status of Accounts",
    page_icon="👋",
)

st.write("# This is the status of your accounts adding future transactions")


# ------------- MAIN CONTENT STARTS HERE --------------------
# get databases and filter only to current date 
db = Db_Connector()

all_data = db.get_all_data_from_all_accounts()
all_data = all_data[all_data['mov_type'] != 'PAYMENT']

max_date = max(all_data['mov_date'])
max_date = max_date.strftime("%B %d %Y")
st.write(f'The Maximun date is: ', max_date)


# Create columns for tables 
col1, col2 = st.columns(2)

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
    st.write('All Accounts Totals: ', pivot_table)

with col2:
    st.write('Only Debit Accounts: ', debits_data)

