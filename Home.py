import streamlit as st
import pandas as pd
import sqlite3
from utils.get_db_data import get_all_data_from_all_accounts

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.write("# Welcome to this Open Personal Finance App 👋")

# st.sidebar.success("")

st.markdown(
    """
    In this App you will be able to control your personal finances all in one place.

    **👈 Select one of the options in the left menu** 
"""
)

# Create columns for tables 
col1, col2 = st.columns(2)

# get databases 
all_data = get_all_data_from_all_accounts()
# print(all_data)

def change_symbol(mov_type, val):
    if mov_type == 'EXPENSES':
        return -val
    else:
        return val

# Define a formatting function
def format_currency(value):
    return '${:,.2f}'.format(value)


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


# select a filter to use to vizualize data by category and by date 
filter_year = st.selectbox('Select the year to filter: ', all_data['MOV_YEAR'].unique().tolist())
filter_month = st.selectbox('Select the month to filter: ', all_data['MOV_MONTH'].unique().tolist())

# filtering data frame 
df_filtered = all_data[(all_data['MOV_YEAR'] == filter_year) & (all_data['MOV_MONTH'] == filter_month) & (all_data['mov_type'].isin(['TRANSFERS', 'INCOME']) == False)]
df_filtered = pd.pivot_table(df_filtered, values='amount', index=['mov_category', 'MOV_YEAR', 'MOV_MONTH'], aggfunc='sum', margins=True)
df_filtered['amount'] = df_filtered['amount'].apply(format_currency)
df_filtered.reset_index(inplace=True, drop=False)
print(df_filtered)

st.write('Expenses by category: ', df_filtered)
