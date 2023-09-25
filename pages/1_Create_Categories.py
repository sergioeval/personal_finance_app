import streamlit as st
import pandas as pd
# import altair as alt
import sqlite3
from utils.get_db_data import get_categories


st.set_page_config(page_title="Create Categories")

st.markdown("# Creating categories in the database")

CATEGORIES_PATH = 'categories/'

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
            # new_category = new_category.strip()
            conn = sqlite3.connect(CATEGORIES_PATH+'categories.db')
            cursor = conn.cursor()

            sql = 'CREATE TABLE IF NOT EXISTS mytable (id INTEGER PRIMARY KEY, category TEXT)'
            cursor.execute(sql)
            conn.commit()

            # check if category exist 
            sql = f"select category from mytable where category='{new_category}'"
            data = pd.read_sql(con=conn, sql=sql)

            if len(data) == 0:
                sql = f"INSERT INTO mytable (category) VALUES ('{new_category}')"
                cursor.execute(sql)
                conn.commit()
            else: 
                st.write(f'The category {new_category} already exists')

   
categ_data , categ_list = get_categories()

st.write('Theese are the available categories: \n', categ_data)