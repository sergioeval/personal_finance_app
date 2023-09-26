import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.general_utils import format_currency
from utils.db_connector import Db_Connector

st.set_page_config(page_title="Dashboard 1")

st.markdown("# All Expenses by Category")

db = Db_Connector()
all_data = db.get_all_data_from_all_accounts() 

df_filtered = all_data[(all_data['mov_type'] == 'EXPENSES')]
df_filtered = df_filtered[['mov_category', 'amount']]
df_filtered = df_filtered.groupby('mov_category').aggregate({'amount': 'sum'})
df_filtered.reset_index(inplace=True, drop=False)


# Overlay values on the bar chart using matplotlib
fig, ax = plt.subplots()
fig.set_facecolor('lightgray')

ax.bar(df_filtered['mov_category'], df_filtered['amount'])

for i, v in enumerate(df_filtered['amount']):
    ax.text(i, v, format_currency(v), ha='center', va='bottom')

st.pyplot(fig)
