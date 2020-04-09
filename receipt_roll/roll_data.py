from datetime import datetime

import pandas as pd
import settings
from receipt_roll import money, common
import numpy as np
import matplotlib.pyplot as plot
import seaborn as sn


def terms_for_index():
    """ Basic structure for holding data with terms as the index. """
    return {'Michaelmas': [], 'Hilary': [], 'Easter': [], 'Trinity': []}


def terms_for_column():
    """ So we can use terms as column headings. """
    return ['Michaelmas', 'Hilary', 'Easter', 'Trinity']


# ---------- Methods used in apply()

def date_to_period(row, freq='D'):
    """ 'Date' is a string. Create a Period. Default is year, month and day. """
    date = row[common.DATE_COL]
    period = pd.Period(date, freq=freq)
    return period


def date_to_month_year_period(row):
    return date_to_period(row, 'M')


def date_to_year_period(row):
    return date_to_period(row, 'Y')


def date_to_week_freq(row):
    return date_to_period(row, 'W-MON')


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


def terms_overview_df():
    """ A data frame that holds summary data about each of the terms_for_index. """

    # columns for this overview
    columns = ['Total Days', 'Days with payments', 'Days with no payments', 'Term total', 'Total entries']

    # data structure to hold calculations
    terms_data = terms_for_index()

    df = roll_with_entities_df()

    # group by terms
    for name, group in df.groupby(common.TERM_COL):
        # number of days in term payments were recorded
        term_days = group[common.DATE_COL].unique().size

        # total amount collected for the term
        term_total = group[common.PENCE_COL].sum()

        # days with no payments
        days_no_payment = group[group[common.DETAILS_COL] == 'NOTHING'][common.DATE_COL].unique().size

        # days with payments
        days_with_payment = term_days - days_no_payment

        # no of entries
        term_entries_no = group[common.DETAILS_COL].count()

        # add the raw data
        terms_data[name].append(term_days)
        terms_data[name].append(days_with_payment)
        terms_data[name].append(days_no_payment)
        terms_data[name].append(term_total)
        terms_data[name].append(term_entries_no)

    return pd.DataFrame.from_dict(terms_data, orient='index', columns=columns)


def payments_overview_df():
    df = roll_with_entities_df()

    data = []

    group_by = df.groupby(common.SOURCE_COL)
    columns = [common.SOURCE_COL, common.PENCE_COL]

    for name, group in group_by:
        if name != 'NOTHING':
            data.append([name.title(), group[common.PENCE_COL].sum()])

    return pd.DataFrame(data=data, columns=columns)


def source_term_payments_matrix_df():
    # get the data
    df = roll_with_entities_df()

    # columns
    terms_names = terms_for_column()

    # indexes (sources)
    sources_names = df[common.SOURCE_COL].unique()

    # create a matrix with values set to zero
    matrix = pd.DataFrame(np.zeros(shape=(len(sources_names), len(terms_names))), columns=terms_names,
                          index=sources_names)

    # group by term
    group_by_term = df.groupby(common.TERM_COL)

    # iterate over the terms
    for term, term_group in group_by_term:

        # for each term, group by source of income, and iterate over each source
        for source, source_group in term_group.groupby(common.SOURCE_COL):
            # get the total for that source
            total = source_group[common.PENCE_COL].sum()
            # update the matrix
            matrix.at[source, term] = total

    # remove 'NOTHING' as a source
    matrix = matrix.drop(index='NOTHING').sort_index()

    # change the source name (index) to title case
    matrix.index = matrix.index.map(str.title)

    return matrix


def days_of_week_total_by_term():
    # get the data
    df = roll_with_entities_df()
    df = df[df[common.SOURCE_COL] != 'NOTHING']

    term_names = terms_for_column()

    # create a matrix with values set to zero
    matrix = pd.DataFrame(np.zeros(shape=(len(term_names), len(common.DAYS_OF_WEEK))), columns=common.DAYS_OF_WEEK,
                          index=term_names)

    for term, term_group in df.groupby(common.TERM_COL):
        for day, day_group in term_group.groupby(common.DAY_COL):
            total = day_group[common.PENCE_COL].sum()
            matrix.at[term, day] = total

    return matrix


