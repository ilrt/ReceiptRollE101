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


def terms_overview_df():
    """ A data frame that holds summary data about each of the terms. """

    # get the data
    df = roll_with_entities_df()

    # data structure to hold calculations
    terms_data = terms()

    group_by = df.groupby(common.TERM_COL)
    columns = ['Total Days', 'Days with payments', 'Days with no payments', 'Term total']

    for name, group in group_by:
        # number of days in term payments were recorded
        term_days = group[common.DATE_COL].unique().size
        # total amount collected for the term
        term_total = group[common.PENCE_COL].sum()
        # days with no payments
        days_no_payment = group[group[common.DETAILS_COL] == 'NOTHING'][common.DATE_COL].unique().size
        # days with payments
        days_with_payment = term_days - days_no_payment

        # add the raw data
        terms_data[name].append(term_days)
        terms_data[name].append(days_with_payment)
        terms_data[name].append(days_no_payment)
        terms_data[name].append(term_total)

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
    df = roll_with_entities_df()
    terms_names = ['Michaelmas', 'Hilary', 'Easter', 'Trinity']
    sources_names = df[common.SOURCE_COL].unique()

    matrix = pd.DataFrame(np.zeros(shape=(len(sources_names), len(terms_names))), columns=terms_names,
                          index=sources_names)

    group_by = df.groupby(common.TERM_COL)
    for term, term_group in group_by:
        for source, source_group in term_group.groupby(common.SOURCE_COL):
            total = source_group[common.PENCE_COL].sum()
            matrix.at[source, term] = total

    return matrix
