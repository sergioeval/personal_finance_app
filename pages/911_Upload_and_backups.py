import streamlit as st
import pandas as pd
import sqlite3
from utils.general_utils import change_symbol, format_currency
import time 
from utils.boxApiJson import BoxApiJson
import glob
from utils.db_connector import Db_Connector

db = Db_Connector()

BOX_CREDS = 'secrets/'
box_api = BoxApiJson(jsonPath=BOX_CREDS+'BoxCredentials.json')
box_accounts_folder_id = '227810718878'
box_categories_folder_id = '227810963459'
ACCOUNTS_PATH = 'accounts/'

st.set_page_config(
    page_title="Upload and backups",
    page_icon="👋",
)


st.write("# Select the action to take ")

# ------------- SIDE BAR FOR BOX UPDATES STARTS HERE ----------------------
with st.form('Box Updates', clear_on_submit=True):
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
            dbs = db.get_unique_account_names_list()
            for db in dbs:
                box_api.uploadNewOrVersion(folderId=box_accounts_folder_id, 
                                           fileName=db, 
                                           filePath=ACCOUNTS_PATH+db)

            #uploading categories 
            box_api.uploadNewOrVersion(folderId=box_categories_folder_id, 
                                       fileName='categories.db', 
                                       filePath='categories/categories.db')



