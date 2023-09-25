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


# get databases 
all_data = get_all_data_from_all_accounts()

# Define a formatting function
def format_currency(value):
    return '${:,.2f}'.format(value)

groups = all_data.groupby(['mov_type']).agg({'amount': 'sum'})
groups['amount'] = groups['amount'].apply(format_currency)

st.write('This is the current total by Transaction Type', groups)

