import streamlit as st
import pandas as pd
from utils.get_db_data import get_all_data_from_an_account
from utils.get_account_dbs import get_account_dataframe

st.set_page_config(
    page_title="Modify Transactions",
    page_icon="👋",
)

st.write("# In here you can modify any transaction")

# in a form filter the account  to modify
# 

#get the accounts names 
accounts_names = get_account_dataframe()
accounts_names = accounts_names['Account_Name'].tolist()

print(accounts_names)
account_data = pd.DataFrame()

with st.form("Modify a Record", clear_on_submit=True):
    st.write('Provide the account of the records to modify\n')
    account_selected = st.selectbox('Select the Account to Modify: ', accounts_names)
    month_number = st.number_input('Provide the month for the record to modify: ')

    submitted = st.form_submit_button("Submit", )

    if submitted:
        account_data = get_all_data_from_an_account(account_db_name = account_selected, month_number=int(month_number))

with st.form("Show Records", clear_on_submit=True):
    st.write('Now Provide the specific record to modify')
    st.write('These are the records from the account and month selected', account_data)

    # create options to select the record ID to modify 
    id_to_modify = st.number_input('What ID do you want to modify: ')
    field_to_modify = st.selectbox('Select the field to modify: ', ['mov_date',
                                                                    'mov_category',
                                                                    'amount'])

    submitted = st.form_submit_button("Submit", )

    if submitted:
        pass
