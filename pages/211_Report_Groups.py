import streamlit as st
import pandas as pd
import sqlite3
from utils.general_utils import change_symbol, format_currency
import time 
from utils.boxApiJson import BoxApiJson
import glob
import datetime
from utils.db_connector import Db_Connector

db =  Db_Connector()

all_data = db.sql_to_df(sql='select * from transactions')
all_data['amount'] = all_data.apply(lambda row: change_symbol(mov_type=row['mov_type'], val=row['amount']), axis=1)
all_data['mov_date'] = pd.to_datetime(all_data['mov_date'])
#print(all_data)

groups_data = db.sql_to_df(sql='select * from date_groups')
groups_data['start_date'] = pd.to_datetime(groups_data['start_date'])
groups_data['end_date'] = pd.to_datetime(groups_data['end_date'])
#print(groups_data)

st.set_page_config(
    page_title="Groups Report",
    page_icon="👋",
)

st.write("## Report by Groups")

data_gruped = pd.DataFrame()

for row in groups_data.itertuples():
    start_date = row[2]
    end_date = row[3]
    label = row[4]
    all_data_temp = all_data.copy()
    all_data_temp = all_data_temp[(all_data_temp['mov_date'] >= start_date) & (all_data_temp['mov_date'] <= end_date)]
    del all_data_temp['id']
    all_data_temp.reset_index(inplace=True, drop=True)
    all_data_temp['GROUP'] = label
    data_gruped = pd.concat([data_gruped, all_data_temp])


data_gruped.sort_values(inplace=True, by='mov_date', ascending=True)
data_gruped = data_gruped.groupby('GROUP').agg({'amount': 'sum'})
data_gruped.reset_index(inplace=True, drop=False)
data_gruped['amount'] = data_gruped['amount'].apply(format_currency)
data_gruped.rename(columns={'amount': 'TOTAL_BALANCE'}, inplace=True)

st.dataframe(data=data_gruped, height=300, width=400)
print(data_gruped)