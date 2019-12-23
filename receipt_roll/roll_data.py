import pandas as pd
import receipt_roll.money as money

# Constants (CSV or data frame column headers)
MEM = 'Membrane'  # The membrane the entry is recorded
TERM = 'Term'  # The term of the entry (Michaelmas, Hilary, Easter and Trinity)
DATE = 'Date'  # The date of the entry, e.g. 1302-07-11
DAY = 'Day'  # The day. e.g. 'Saturday'
SOURCE = 'Source'  # The source (often geographical), e.g. 'DUBLIN'
ENTRY = 'Entry'  # Entry details, e.g. 'The same Nicholas, ½ mark for falsely raising hue and cry.'
VAL = 'Value'  # Value extracted from the details. e.g. '½ mark'
PENCE = 'Pennies'  # The pence equivalent of the value, easier for comparisons


def roll_as_df():
    """ Return the CSV file as a pandas data frame"""
    return pd.read_csv('roll.csv')


def daily_sum_df(df):
    """ Create a new data frame of daily sums in pence and the equivalent £.s.d. """

    data = []
    columns = [DATE, PENCE, '£.s.d.']

    date_group = df.groupby(DATE)

    for date, group in date_group:
        pence = int(group[PENCE].sum())
        row = [date, pence, money.pennies_to_psd(pence)]
        data.append(row)

    return pd.DataFrame(data, columns=columns)
