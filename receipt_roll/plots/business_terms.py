""" The following plots are used to illustrate business and income on the various terms. """

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from receipt_roll import common, money
from receipt_roll.data import roll
from receipt_roll.plots.base import save_or_show, set_labels_title, SN_STYLE
from receipt_roll.plots.radar import plot_radar


# ---------- Monthly look at totals and business (line plots)

def plt_monthly_total(save=False, file_name='plt_monthly_total.png', file_format='png'):
    """ Show the monthly totals in a line plot. """

    # get the data
    df = roll.roll_with_entities_df()

    # set the style
    sns.set(style=SN_STYLE)

    # tick range in pence (divisible by 240, which is £1)
    ticks_range = np.arange(0, 480000, 120000)

    # show the labels as £ rather than pennies
    ticks_labels = []
    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plt.yticks(ticks_range, ticks_labels)

    # create a frequency by year, month
    df['year_month'] = df.apply(roll.date_to_month_year_period, axis=1)
    ax = df.groupby(df.year_month)[common.PENCE_COL].sum().plot(marker='o')
    ax.autoscale(True)

    # add labels etc.
    set_labels_title('Months', 'Total payments', 'Total payments per month ')

    save_or_show(save, file_name, file_format)


def plt_monthly_business_count(save=False, file_name='plt_monthly_business.png', file_format='png'):
    """ Show the monthly counts of business in a line plot. """

    # get the data
    df = roll.roll_with_entities_df()

    # set the style
    sns.set(style=SN_STYLE)

    # create a frequency by year, month
    df['year_month'] = df.apply(roll.date_to_month_year_period, axis=1)
    ax = df.groupby(df.year_month)[common.DETAILS_COL].count().plot(marker='o')
    ax.autoscale(True)

    # add labels etc.
    set_labels_title('Months', 'Count of transactions', 'Total transactions per month ')

    save_or_show(save, file_name, file_format)


def plt_transactions_and_totals_by_month(save=False, file_name='plt_transactions_and_totals_by_month.png',
                                         file_format='png'):
    """ Plot the total count of transactions (business recorded) and the total value of that business, per month,
        as a % of the total count of transactions and the total value of business for the whole financial year. """

    # set the style
    sns.set(style=SN_STYLE)

    # get the data
    df = roll.roll_with_entities_df()

    # clear empty days
    df = df[df[common.SOURCE_COL] != 'NOTHING']

    # month and year period
    df['year_month'] = df.apply(roll.date_to_month_year_period, axis=1)

    trans_pc = 'No. of transactions as % of total'
    total_pc = 'Total value of transactions as % of total'

    columns = [trans_pc, total_pc]
    index = df['year_month'].unique()

    pence_count = df[common.PENCE_COL].count()
    pence_sum = df[common.PENCE_COL].sum()

    matrix = pd.DataFrame(np.zeros(shape=(len(index), len(columns))), columns=columns, index=index)

    for month, month_group in df.groupby(df.year_month):
        matrix.at[month, trans_pc] = month_group[common.PENCE_COL].count() / pence_count * 100
        matrix.at[month, total_pc] = month_group[common.PENCE_COL].sum() / pence_sum * 100

    # plot
    ax = matrix.plot(marker='o')
    ax.autoscale(True)

    # add labels etc.
    set_labels_title('Months', '% of total', 'No. of transactions and their total value, \nper month, as a % of the '
                                             'total for the year')

    save_or_show(save, file_name, file_format)


# ---------- Weekly look at totals and business (line plots)

def plt_total_receipts_by_week_and_term(save=False, file_name='plt_total_receipts_by_week_and_term.png',
                                        file_format='png'):
    """ Create a line plot for the total value of the receipts received in each week of a term. Each term
        is plotted on its own line. """

    # set the style
    sns.set(style=SN_STYLE)

    # get data and remove 'NOTHING' values
    df = roll.roll_with_entities_df()
    df = df[df[common.SOURCE_COL] != 'NOTHING']

    # tick range in pence (divisible by 240, which is £1)
    ticks_range = np.arange(0, 240000, 24000)

    # show the labels as £ rather than pennies
    ticks_labels = []
    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plt.yticks(ticks_range, ticks_labels)

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        values = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].sum()
        sns.lineplot(y=values, x=values.index, label=term, marker='o')

    # add labels etc.
    set_labels_title('Week', 'Total value of receipts', 'Total value of receipts for each week of the term')

    save_or_show(save, file_name, file_format)


def plt_total_receipts_by_week_and_term_as_pc_of_year_total(save=False,
                                                            file_name='plt_total_receipts_week_term_pc_year_total.png',
                                                            file_format='png'):
    """ Create a line plot for the total value of the receipts received in each week of a term as a percentage
        of the total receipts over the year. Each term is plotted on its own line. """

    # set the style
    sns.set(style=SN_STYLE)

    # get data and remove 'NOTHING' values
    df = roll.roll_with_entities_df()
    df = df[df[common.SOURCE_COL] != 'NOTHING']

    # total for the year
    total = df[common.PENCE_COL].sum()

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        values = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].sum() / total * 100
        sns.lineplot(y=values, x=values.index, label=term, marker='o')

    # add labels etc.
    set_labels_title('Week', 'Value of receipts as % of year total',
                     'Total value of weekly receipts as a % of the yearly total')

    save_or_show(save, file_name, file_format)


def plt_transactions_count_by_week_and_term(save=False, file_name='plt_transactions_count_by_week_and_term.png',
                                            file_format='png'):
    """ Create a line plot for the total number of transactions over the year. Each term is plotted on its own line. """

    # set the style
    sns.set(style=SN_STYLE)

    # get data and remove 'NOTHING' values
    df = roll.roll_with_entities_df()
    df = df[df[common.SOURCE_COL] != 'NOTHING']

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        values = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].count()
        sns.lineplot(y=values, x=values.index, label=term, marker='o')

    # add labels etc.
    set_labels_title('Week', 'No. of transactions',
                     'No. of transactions for each week of the term')

    save_or_show(save, file_name, file_format)


def plt_transactions_count_by_week_and_term_as_pc_of_year_total(save=False,
                                                                file_name='plt_transactions_week_term_pc_year_total.png',
                                                                file_format='png'):
    """ Create a line plot for the total number of transactions as a percentage of the total number of transactions
        over the year. Each term is plotted on its own line. """

    # set the style
    sns.set(style=SN_STYLE)

    # get data and remove 'NOTHING' values
    df = roll.roll_with_entities_df()
    df = df[df[common.SOURCE_COL] != 'NOTHING']

    # total for the year
    total = df[common.PENCE_COL].count()

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        values = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].count() / total * 100
        sns.lineplot(y=values, x=values.index, label=term, marker='o')

    # add labels etc.
    set_labels_title('Week', 'Value of receipts as % of year total',
                     'Number of weekly transactions as a % of the yearly total')

    save_or_show(save, file_name, file_format)


def plt_transactions_total_as_pc_of_term(save=False, file_name='plt_transactions_total_as_pc_of_term.png',
                                         file_format='png'):
    """ Plot each term with the total value and amount of transactions as a percentage of the total for
        that term rather than the year. """

    # set the style
    sns.set(style=SN_STYLE)

    # get data and remove 'NOTHING' values
    df = roll.roll_with_entities_df()
    df = df[df[common.SOURCE_COL] != 'NOTHING']

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        # total for the term
        total_count = term_group[common.PENCE_COL].count()
        total_sum = term_group[common.PENCE_COL].sum()
        values_count = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].count() / total_count * 100
        sns.lineplot(y=values_count, x=values_count.index, label='Transaction count as %',
                     marker='o')
        values_sum = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].sum() / total_sum * 100
        sns.lineplot(y=values_sum, x=values_sum.index, label='Total receipts as %', marker='o')

        # add labels etc.
        set_labels_title('Week', '% of term total',
                         '{}\n Number of weekly transactions and total receipts as a % of the term total'.format(term))
        plt_file_name = "{}_{}".format(term.lower(), file_name)
        save_or_show(save, plt_file_name, file_format)


def plt_sheriff_total_by_week(term_name='Michaelmas', save=False, file_name='plt_sheriff_total_by_week.png',
                              file_format='png'):

    # set the style
    sns.set(style=SN_STYLE)

    # get data
    df = roll.roll_with_entities_df()
    term_df = df[df[common.TERM_COL] == term_name]

    # columns and index based on number of weeks in the term
    cols = ['Weekly total sum', 'Weekly sum from sheriff']
    weeks_of_term = np.arange(term_df[common.WEEK_COL].min(), term_df[common.WEEK_COL].max())
    totals_df = pd.DataFrame(np.zeros(shape=(len(weeks_of_term), len(cols))), columns=cols, index=weeks_of_term)

    # find sheriffs ...
    for week, week_group in term_df.groupby(common.WEEK_COL):
        totals_df.at[week, cols[1]] = week_group[week_group[common.DETAILS_COL].str.contains('sheriff')][
            common.PENCE_COL].sum()
        totals_df.at[week, cols[0]] = week_group[common.PENCE_COL].sum()

    totals_df.plot()

    max_value = totals_df[cols[0]].max()
    top_range = (math.ceil(max_value / 12000)) * 12000
    ticks_range = np.arange(0, top_range + 12000, 12000)

    ticks_labels = []
    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plt.yticks(ticks_range, ticks_labels)

    # add labels etc.
    set_labels_title('Week', 'Value of receipts',
                     'Value of receipts returned by sheriffs in {}'.format(term_name))

    save_or_show(save, file_name, file_format)


# ---------- Radar plots


def plt_terms_business_radar(save=False, file_name='plt_terms_business_radar.png', file_format='png'):
    """ Create four radar charts that show the relationship, for each term, between the length of the term,
        the amount of business (transactions) and total amount of receipts. """

    # get the data
    df = roll.roll_with_entities_df()

    # create an empty data frame to hold the summary data
    categories = ['Days', 'Transactions', 'Income']
    radar_df = pd.DataFrame(np.zeros(shape=(len(categories), len(common.TERMS))),
                            columns=common.TERMS, index=categories)

    # ----- Length of the terms (as a % of the total)

    # temp structure to track the start and end dates of each term
    days = {}

    # create a Period from the date
    df['Period'] = df.apply(roll.date_to_period, axis=1)

    # get the  start and end dates for each term
    for term, term_group in df.groupby(common.TERM_COL):
        start_day = term_group['Period'].min()
        end_day = term_group['Period'].max()
        period_range = pd.period_range(start_day, end_day)
        days[term] = len(period_range)

    # total amount of days
    total_terms_days = sum(days.values())

    # update the radar data frame with the % values
    for key in days.keys():
        radar_df.at[categories[0], key] = days[key] / total_terms_days * 100

    # ----- Number of transactions (as a % of the total)

    # total transaction over the year
    total_transactions = df[common.PENCE_COL].count()

    # transactions as a % added to the radar data frame
    for term, term_group in df.groupby(common.TERM_COL):
        terms_transaction = term_group[common.PENCE_COL].count()
        radar_df.at[categories[1], term] = terms_transaction / total_transactions * 100

    # ----- Value of transactions (as a % of the total)

    # total amount received
    total_payments = df[common.PENCE_COL].sum()

    # amount as a % added to the radar data frame
    for term, term_group in df.groupby(common.TERM_COL):
        terms_payments = term_group[common.PENCE_COL].sum()
        radar_df.at[categories[2], term] = terms_payments / total_payments * 100

    # colours to use in the plots (one for each term)
    colours = ['#F06292', '#FFB74D', '#64B5F6', '#81C784']

    # create a chart for each term
    for idx, term in enumerate(common.TERMS):
        values = radar_df.loc[:, term].values.flatten().tolist()
        plt_file_name = "{}_{}".format(term.lower(), file_name)
        plot_radar(categories, values, term, colours[idx], save, plt_file_name, file_format)
