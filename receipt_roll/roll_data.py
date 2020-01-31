import pandas as pd
import settings
from receipt_roll import money, common
import numpy as np
import matplotlib.pyplot as plot
import seaborn as sn


def terms():
    """ Basic structure for holding around terms """
    return {'Michaelmas': [], 'Hilary': [], 'Easter': [], 'Trinity': []}


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
    """ A data frame that holds summary data about each of the terms. """

    # get the data
    df = roll_with_entities_df()

    # data structure to hold calculations
    terms_data = terms()

    # total payments
    total_payments = df[common.PENCE_COL].sum()

    # total number of payment days
    total_days = df[common.DATE_COL].unique().size

    group_by = df.groupby(common.TERM_COL)
    columns = ['Days', '% of days', 'Term total', 'Term % of total', 'Mean daily', 'Median daily', 'Mode daily']

    for name, group in group_by:
        # number of days in term payments were recorded
        term_days = group[common.DATE_COL].unique().size
        # total amount collected for the term
        term_total = group[common.PENCE_COL].sum()
        # % of total collected in a term
        pc = term_total / total_payments * 100
        # days % of total
        days_pc = term_days / total_days * 100
        # mean daily payment
        day_pay_mean = group[common.PENCE_COL].mean()
        # median payment
        day_pay_median = group[common.PENCE_COL].median()
        # mode payment
        day_pay_mode = group[common.PENCE_COL].mode()[0]

        # add the data
        terms_data[name].append(term_days)
        terms_data[name].append(days_pc)
        terms_data[name].append(term_total)
        terms_data[name].append(pc)
        terms_data[name].append(day_pay_mean)
        terms_data[name].append(day_pay_median)
        terms_data[name].append(day_pay_mode)

    return pd.DataFrame.from_dict(terms_data, orient='index', columns=columns)
