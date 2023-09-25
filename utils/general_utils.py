
'''
General functions for different usage
'''


def change_symbol(mov_type, val):
    if mov_type == 'EXPENSES':
        return -val
    else:
        return val


# Define a formatting function
def format_currency(value):
    return '${:,.2f}'.format(value)


