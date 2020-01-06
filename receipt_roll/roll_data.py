import pandas as pd
import settings
from receipt_roll import money, common


def roll_as_df():
    """ Return the CSV file as a pandas data frame"""
    return pd.read_csv(settings.ROLL_CSV)


def daily_sum_from_roll_df(df):
    """ Create a new data frame of daily sums in pence and the equivalent £.s.d. from the roll data """

    data = []
    columns = [common.DATE_COL, common.PENCE_COL, common.PSD_COL]

    date_group = df.groupby(common.DATE_COL)

    for date, group in date_group:
        pence = int(group[common.PENCE_COL].sum())
        row = [date, pence, money.pence_to_psd(pence)]
        data.append(row)

    return pd.DataFrame(data, columns=columns)
