import pandas as pd
import settings
from receipt_roll import money, common
import numpy as np
import matplotlib.pyplot as plot
import seaborn as sn


def roll_as_df():
    """ Return the CSV file as a pandas data frame"""
    return pd.read_csv(settings.ROLL_CSV)


def daily_sums_df():
    """ Return the CSV file with the daily sums """
    return pd.read_csv(settings.DAILY_SUMS_CSV)


def daily_sum_from_roll_df(df):
    """ Create a new data frame of daily sums in pence and the equivalent £.s.d. from the roll data """

    data = []
    columns = [common.DATE_COL, common.PENCE_COL, common.PSD_COL]

    date_group = df.groupby(common.DATE_COL)

    for date, group in date_group:
        pence = group[common.PENCE_COL].sum()
        row = [date, pence, money.pence_to_psd(pence)]
        data.append(row)

    return pd.DataFrame(data, columns=columns)


def roll_with_entities_df():
    """ Return the CSV file of the roll with entities as a pandas data frame"""
    return pd.read_csv(settings.ROLL_WITH_ENTITIES_CSV)


def compare_daily_sums_df():
    """ Return the comparison files as a Pandas data frame. """
    return pd.read_csv(settings.DAILY_SUMS_COMPARE_CSV)


def total_by_terms_df():
    df = roll_with_entities_df()

    terms = {'Michaelmas': [], 'Hilary': [], 'Easter': [], 'Trinity': []}

    total = df[common.PENCE_COL].sum()

    group_by = df.groupby(common.TERM_COL)
    columns = ['Pence', '%', '£.s.d.']

    for name, group in group_by:
        term_total = group[common.PENCE_COL].sum()
        pc = term_total / total * 100
        psd = money.pence_to_psd(term_total)
        terms[name].append(term_total)
        terms[name].append(pc)
        terms[name].append(psd)

    return pd.DataFrame.from_dict(terms, orient='index', columns=columns)


