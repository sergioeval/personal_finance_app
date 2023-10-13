
'''
General functions for different usage
'''
import datetime




def change_symbol(mov_type, val):
    if mov_type == 'CREDIT_PAYMENT':
        return -val
    else:
        return val


# Define a formatting function
def format_currency(value):
    return '${:,.2f}'.format(value)


def get_number_days_to_transactions(mov_date):
    cur_date = datetime.datetime.now()
    days_to_transaction = (mov_date - cur_date).days
    return days_to_transaction



