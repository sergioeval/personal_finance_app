import pandas as pd
# import os
import glob

ACCOUNTS_PATH = 'accounts/'


def get_account_dataframe():

    account_list = glob.glob(ACCOUNTS_PATH+'*.db', recursive=True)

    account_list = [acc.split('/')[1] for acc in account_list]

    accounts_data = []
    for acc in account_list:
        temp = {
            'Account_Name': acc
        }
        accounts_data.append(temp)

    acc_df = pd.DataFrame(accounts_data)
    return acc_df