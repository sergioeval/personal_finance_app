import streamlit as st
import pandas as pd
# import altair as alt
import sqlite3
from utils.get_db_data import get_categories
from utils.db_connector import Db_Connector


st.set_page_config(page_title="Create Categories")

st.markdown("# Creating categories in the database")

db_connector = Db_Connector()

# form for the category creation
# form 
with st.form("new_categories", clear_on_submit=True):
   st.write("Create the categories for your transactions (Example: House Services, Groceries, Pharmacy,  etc)")

   new_category = st.text_input('New Category')

    # Every form must have a submit button.
   submitted = st.form_submit_button("Submit", )

   if submitted:
        if new_category:
            new_category = new_category.strip().upper().replace(' ', '_')

            # Create table if not exists 
            sql = 'CREATE TABLE IF NOT EXISTS mytable (id INTEGER PRIMARY KEY, category TEXT)'
            db_connector.modify_db_sql(sql=sql,  is_category_db=True)

            # check if category exist 
            sql = f"select category from mytable where category='{new_category}'"
            data = db_connector.sql_to_df(sql=sql, is_category_db=True)

            if len(data) == 0:
                sql = f"INSERT INTO mytable (category) VALUES ('{new_category}')"
                db_connector.modify_db_sql(sql=sql, is_category_db=True)
            else: 
                st.write(f'The category {new_category} already exists')

   
categ_data = db_connector.sql_to_df(sql='select category from mytable', 
                                    is_category_db=True)


st.write('Theese are the available categories: \n', categ_data)
