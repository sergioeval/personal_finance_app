import streamlit as st
import pandas as pd
from utils.db_connector import Db_Connector

st.set_page_config(
    page_title="Update Categories",
    page_icon="👋",
)

st.write("# In here you can modify all Categories")

# Planning 
#'''
#- Create a state session key for category_selected and initialize it with None
#- Get all the category names in a list 
#- Create a selectbox to select the category to modify 
#- Modify the Category in the category database first 
#- Get a list of all the accounts 
#- Loop over the account list and in each database:
#    - change the category where the category is = to category_selected 
#'''

#- Create a state session key for category_selected and initialize it with None
if 'category_selected' not in st.session_state:
    st.session_state.category_selected = None

if 'new_category' not in st.session_state:
    st.session_state.new_category = None

if 'new_categ_exists' not in st.session_state:
    st.session_state.new_categ_exists = 'tbd'

#- Get all the category names in a list 
connector = Db_Connector()
category_list = connector.get_unique_categories_list()

#- Create a selectbox to select the category to modify 
with st.form('Select category', clear_on_submit=True):
    st.write('Select The Category to modify')
    category = st.selectbox('Category Selection:', category_list)
    st.write('Provide the new Category Name')
    new_category_name = st.text_input('New Category Name: ')

    submitted = st.form_submit_button('Submit', )

    if submitted:
        st.session_state.category_selected = category
        st.session_state.new_category = new_category_name.strip().upper().replace(' ', '_')


#- Modify the Category in the category database first 
with open('sql_templates/update_category_categorydb.sql', mode='r') as f:
    sql_categ_categdb_template = f.read()

# check if the new category exist. 
if st.session_state.new_category:
    st.session_state.new_categ_exists = connector.check_if_exist_category_name(category_name=st.session_state.new_category)

if st.session_state.new_categ_exists == 'not_exists':
    # make modifications 
    connector.update_record_category(sql=sql_categ_categdb_template, 
                                     old_categ=st.session_state.category_selected, 
                                     new_categ=st.session_state.new_category)




