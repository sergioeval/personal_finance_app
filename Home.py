import streamlit as st
import pandas as pd
import sqlite3
from utils.get_db_data import get_all_data_from_all_accounts
from utils.get_account_dbs import get_account_dataframe
from utils.general_utils import change_symbol, format_currency
import time 
from utils.boxApiJson import BoxApiJson
import glob

BOX_CREDS = 'secrets/'
box_api = BoxApiJson(jsonPath=BOX_CREDS+'BoxCredentials.json')
box_accounts_folder_id = '227810718878'
box_categories_folder_id = '227810963459'
ACCOUNTS_PATH = 'accounts/'

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.write("# Welcome to this Open Personal Finance App 👋")

with st.sidebar.form('Box Updates', clear_on_submit=True):
    st.markdown('### This action will update your local databases or upload your local databases to box.')
    box_action_confirm = st.selectbox('Select an action to perform: ', ['NONE', 'DOWNLOAD_DATABASES', 'UPLOAD_DATABASES'])
    
    # submit button 
    submitted = st.form_submit_button('Perform Action')

    
    if submitted:
        if box_action_confirm.upper() == 'DOWNLOAD_DATABASES':
            print('DOWNLOADING')
            # Get items from folder 
            items = box_api.getItemsFromFolder(folderId=box_accounts_folder_id)
            print(items)
            #dbs = dbs['Account_Name'].tolist()
            for item in items:
                # download all databases in the list  
                box_api.downloadFile(fileId=item['item_id'], 
                                     filePath=ACCOUNTS_PATH+item['item_name'])

            # dwnloading file from categories 
            items = box_api.getItemsFromFolder(folderId = box_categories_folder_id)

            for item in items:
                box_api.downloadFile(fileId = item['item_id'], 
                                     filePath ='categories/'+item['item_name'])

        if box_action_confirm.upper() == 'UPLOAD_DATABASES':
            print('UPLOADING')
            # uploading accounts 
            dbs = get_account_dataframe()
            dbs = dbs['Account_Name'].tolist()
            for db in dbs:
                box_api.uploadNewOrVersion(folderId=box_accounts_folder_id, 
                                           fileName=db, 
                                           filePath=ACCOUNTS_PATH+db)

            #uploading categories 
            box_api.uploadNewOrVersion(folderId=box_categories_folder_id, 
                                       fileName='categories.db', 
                                       filePath='categories/categories.db')


st.markdown(
    """
    In this App you will be able to control your personal finances all in one place.

    **👈 Select one of the options in the left menu** 

    Start by creating new accounts and categories.
"""
)

# Create columns for tables 
col1, col2 = st.columns(2)

# get databases 
all_data = get_all_data_from_all_accounts()
# print(all_data)

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

st.markdown('# In this section you can see all your expenses by YEAR, MONTH and Category')
st.write('Select your filters')
# select a filter to use to vizualize data by category and by date 
filter_year = st.selectbox('Select the year to filter: ', all_data['MOV_YEAR'].unique().tolist())
filter_month = st.selectbox('Select the month to filter: ', all_data['MOV_MONTH'].unique().tolist())

# filtering data frame 
df_filtered = all_data[(all_data['MOV_YEAR'] == filter_year) & (all_data['MOV_MONTH'] == filter_month) & (all_data['mov_type']=='EXPENSES')]
df_filtered = pd.pivot_table(df_filtered, values='amount', index=['mov_category', 'MOV_YEAR', 'MOV_MONTH'], aggfunc='sum', margins=True)
df_filtered['amount'] = df_filtered['amount'].apply(format_currency)
df_filtered.reset_index(inplace=True, drop=False)
#print(df_filtered)

st.write('Expenses by category: ', df_filtered)
