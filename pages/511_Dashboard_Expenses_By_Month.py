import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.general_utils import format_currency
from utils.db_connector import Db_Connector

st.set_page_config(page_title="Dashboard 1")

st.markdown("# All Expenses by Category")
st.markdown('# In this section you can see all your expenses by YEAR, MONTH and Category')
st.write('Select your filters')

db = Db_Connector()
all_data = db.get_all_data_from_all_accounts() 
all_data = all_data[all_data['mov_type'] != 'PAYMENT']

# select a filter to use to vizualize data by category and by date 
filter_year = st.selectbox('Select the year to filter: ', all_data['MOV_YEAR'].unique().tolist())
filter_month = st.selectbox('Select the month to filter: ', all_data['MOV_MONTH'].unique().tolist())

# filtering data frame 
df_filtered = all_data[(all_data['MOV_YEAR'] == filter_year) & 
                       (all_data['MOV_MONTH'] == filter_month) & 
                       (all_data['mov_type']=='EXPENSES')]


#df_filtered = all_data[(all_data['mov_type'] == 'EXPENSES')]
df_filtered = df_filtered[['mov_category', 'amount']]
df_filtered = df_filtered.groupby('mov_category').aggregate({'amount': 'sum'})
df_filtered.reset_index(inplace=True, drop=False)

# get the total Expenses 
total = format_currency(df_filtered['amount'].sum())
st.write(f'# The Total of Expenses in this Month is: {total}')

# Overlay values on the bar chart using matplotlib
fig, ax = plt.subplots()
fig.set_facecolor('lightgray')

ax.bar(df_filtered['mov_category'], df_filtered['amount'])
plt.xticks(rotation=90)
for i, v in enumerate(df_filtered['amount']):
    ax.text(i, v, format_currency(v), ha='center', va='bottom')
st.pyplot(fig)
