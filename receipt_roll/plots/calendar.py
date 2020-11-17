import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

from receipt_roll import roll_data, common
from receipt_roll.plots.base import months_labels_cal, SN_STYLE, FONT_NAME


def calendar_empty_matrix():
    """ An empty data frame with months (1-12) as an index and days (1-31) as columns. """

    # days have upto 31 days
    days = np.arange(1, 31 + 1, 1)

    # months (numerical), starting in September
    months = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]

    # create an empty data frame, that represents days (columns) and months (rows)
    cal = pd.DataFrame(np.zeros(shape=(len(months), len(days))), columns=days, index=months)

    # populate cal data frame with 1 for actual days in the month, i.e. there is no 31 September
    cal_period = pd.period_range('1301-09-01', '1302-08-31')
    for period in cal_period:
        cal.at[period.month, period.day] = 1

    return cal


def calender_heat_map(data, cmap, norm, title):
    """ Basic rendering of the heatmap to make it look like a calendar. """
    sns.set(style=SN_STYLE, font=FONT_NAME)

    plt.figure(figsize=(8, 6))

    sns.heatmap(data, cmap=cmap, norm=norm, cbar=False)

    plt.ylabel('Months')
    plt.xlabel('Days')

    plt.yticks(rotation=0)
    plt.xticks(rotation=0)


def plt_terms_calendar():
    """ Plot that use a heatmap to show the terms against available days in a month. It illustrates the
        holidays that the Exchequer wasn't sitting. """

    cal = calendar_empty_matrix()

    # get the data
    data = roll_data.roll_with_entities_df()

    # make a pandas column of pandas Period types from the date
    data['date_period'] = data.apply(roll_data.date_to_period, axis=1)

    # populate the cal data frame with '2' for term term dates
    for term, term_period in data.groupby(common.TERM_COL, sort=False):
        term_range = pd.period_range(term_period.date_period.min(), term_period.date_period.max())
        for period in term_range:
            cal.at[period.month, period.day] = 2

    # change index to month labels
    cal.index = months_labels_cal

    # set the colours for the heatmap
    cmap = mpl.colors.ListedColormap(['#ffffff', '#f2f4f4', '#bdc3c7'])
    norm = mpl.colors.BoundaryNorm([0, 1, 2, 3], cmap.N)

    # create the plot
    calender_heat_map(cal, cmap, norm,
                      'Terms in the 1301/2 financial year\n derived from (The National Archives, London, E 101/233/16')

    # add the days of the terms to the plot
    plt.text(13, 2, 'Michaelmas')
    plt.text(13, 6, 'Hilary')
    plt.text(13, 8.6, 'Easter')
    plt.text(13, 10.6, 'Trinity')

    plt.show()


def plt_terms_calendar_payments():
    """ Plot that use a heatmap to show the terms against available days in a month. It illustrates the
        days payments were received. """

    # get the data
    data = roll_data.roll_with_entities_df()

    # make a pandas column of pandas Period types from the date
    data['date_period'] = data.apply(roll_data.date_to_period, axis=1)

    # create an empty data frame, that represents days (columns) and months (rows)
    cal = calendar_empty_matrix()

    # populate the cal data frame with '2' for term term dates
    for term, term_period in data.groupby(common.TERM_COL, sort=False):
        term_range = pd.period_range(term_period.date_period.min(), term_period.date_period.max())
        for period in term_range:
            cal.at[period.month, period.day] = 2

    for term_day, term_group in data.groupby(data.date_period):
        if term_group[common.PENCE_COL].sum() > 0:
            cal.at[term_day.month, term_day.day] = 3

    feasts_nothing = pd.read_csv('data/feast_nothing.csv')
    no_payments = feasts_nothing[feasts_nothing['Details'].isnull()]['Date']
    for date in no_payments:
        period = pd.Period(date)
        cal.at[period.month, period.day] = 4

    # change index to month labels
    cal.index = months_labels_cal

    # set the colours for the heatmap
    cmap = mpl.colors.ListedColormap(['#ffffff', '#f2f4f4', '#bdc3c7', '#797d7f', '#000000'])
    norm = mpl.colors.BoundaryNorm([0, 1, 2, 3, 4, 5], cmap.N)

    # create the plot
    calender_heat_map(cal, cmap, norm,
                      'Terms and days with payments in the 1301/2 financial year\n derived from '
                      '(The National Archives, London, E 101/233/16')

    plt.show()
