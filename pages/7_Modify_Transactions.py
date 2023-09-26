import streamlit as st
import pandas as pd
from utils.db_connector import Db_Connector

st.set_page_config(
    page_title="Modify Transactions",
    page_icon="👋",
)

st.write("# In here you can modify any transaction")

db = Db_Connector()

# in a form filter the account  to modify
# 

#get the accounts names 
accounts_names = db.get_unique_account_names_list() 

account_data = pd.DataFrame()

with open('sql_templates/update_value_template.sql', mode='r') as f:
    sql_update_template = f.read()

if 'account' not in st.session_state:
    st.session_state.account = None
if 'record_id' not in st.session_state:
    st.session_state.record_id = None
if 'field' not in st.session_state:
    st.session_state.field = None

# form to select the account to modify 
with st.form("Modify a Record", clear_on_submit=True):
    st.write('Provide the account of the records to modify\n')
    account_selected = st.selectbox('Select the Account to Modify: ', accounts_names)
    month_number = st.number_input('Provide the month for the record to modify: ')

    submitted = st.form_submit_button("Submit", )

    if submitted:
        st.session_state.account = account_selected
        account_data = db.get_data_from_account_and_month(db_name=account_selected, 
                                                          month_number=int(month_number))


with st.form("Show Records", clear_on_submit=True):
    st.write('Now Provide the specific record to modify')
    if st.session_state.account != None:
        st.warning(f'YOU SELECTED THE ACCOUNT: {st.session_state.account}')
    st.write('These are the records from the account and month selected', account_data)

    # create options to select the record ID to modify 
    id_to_modify = st.number_input('What ID do you want to modify: ')
    field_to_modify = st.selectbox('Select the field to modify: ', ['mov_date',
                                                                    'mov_category',
                                                                    'amount'])

    submitted = st.form_submit_button("Submit", )

    if submitted:
        st.session_state.record_id = int(id_to_modify)
        st.session_state.field = field_to_modify


with st.form('final_form_modification', clear_on_submit=True):
    st.write('Now provide the new Value')

    if st.session_state.record_id != None:
        st.warning(f'Account Selected: {st.session_state.account} - Record Id selected: {st.session_state.record_id} - Field to Modify: {st.session_state.field}')

    if st.session_state.record_id == None:
        st.write('You need to select data in the first and second form')

    if st.session_state.field == 'mov_date':
        new_value = st.date_input('Select the new mov_date')

    if st.session_state.field == 'mov_category':
        new_value = st.selectbox('Select the new Category: ', db.get_unique_categories_list())

    if st.session_state.field == 'amount':
        new_value = st.number_input('Provide the new Amount: ')

    submitted = st.form_submit_button("Submit", )

    if submitted:
        sql_update_template = sql_update_template.format(st.session_state.field)
        db.update_record_accounts(db_name=st.session_state.account, 
                                  sql = sql_update_template, 
                                  new_value = new_value, 
                                  record_id = st.session_state.record_id) 
        pass
