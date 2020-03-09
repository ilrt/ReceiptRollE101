from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plot
import seaborn as sns
from receipt_roll import roll_data, money, common
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

BASIC_PLOT_TITLE = "{} \n in the 1301–2 receipt roll of the Irish Exchequer \n (The National Archives, London, " \
                   "E 101/233/16) "

PLOT_DIMENSIONS = (6, 5)
TITLE_FONT_SIZE = 12
LABEL_FONT_SIZE = 10
ANNOTATION_FONT_SIZE = 8

SN_STYLE = 'darkgrid'

# months (labels)
months_labels_cal = ['[1301] Sep', 'Oct', 'Nov', 'Dec', '[1302] Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']


def to_date(row):
    return datetime.strptime(str(row['Date']), '%Y-%m-%d')


def filter_out_nothing(df):
    """ Filter out rows where no receipts are recorded. """
    return df[df[common.SOURCE_COL] != 'NOTHING']


def set_labels_title(x_label, y_label, title):
    """ Helper text to set x and y labels and title for a plot. """
    plot.xlabel(x_label, fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.ylabel(y_label, fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.title(BASIC_PLOT_TITLE.format(title), fontsize=TITLE_FONT_SIZE, fontweight='bold')


def plt_total_by_terms():
    """ A basic bar graph that shows the payments by term.  """

    # set a plot size
    plot.figure(figsize=PLOT_DIMENSIONS)

    # get the totals
    terms_df = roll_data.terms_overview_df()

    # tick range in pence (divisible by 240, which is £1)
    ticks_range = np.arange(0, 600000, 120000)

    # show the labels as £ rather than pennies
    ticks_labels = []
    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plot.yticks(ticks_range, ticks_labels)

    # plot the data
    ax = sns.barplot(x=terms_df.index, y=terms_df['Term total'])

    # add the £.s.d. to each bar
    for patch, pence in zip(ax.patches, terms_df['Term total']):
        ax.text(patch.get_x() + patch.get_width() / 2, patch.get_height(), money.pence_to_psd(pence), ha="center",
                fontsize=ANNOTATION_FONT_SIZE, linespacing=2.0)

    # add labels
    plot.ylabel('Total payments', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.xlabel('Terms', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.title(BASIC_PLOT_TITLE.format('Total payments, per term, '), fontsize=TITLE_FONT_SIZE, fontweight='bold')

    # display the bar
    plot.show()


def plt_pc_by_terms():
    """ A basic bar graph that shows the payments by term as a percentage.  """

    # set a plot size
    plot.figure(figsize=(6, 6))

    # get the dataset
    terms_df = roll_data.terms_overview_df()

    # calculate the total income
    total = terms_df['Term total'].sum()

    # work out the %
    term_total_as_pc = terms_df['Term total'] / total * 100

    # plot the data
    ax = sns.barplot(x=term_total_as_pc.index, y=term_total_as_pc)

    # add the £.s.d. to each bar
    for patch, pc in zip(ax.patches, term_total_as_pc):
        ax.text(patch.get_x() + patch.get_width() / 2, patch.get_height(), '{0:.1f}%'.format(pc), ha="center",
                fontsize=ANNOTATION_FONT_SIZE, linespacing=2.0)

    # add labels
    plot.ylabel('% of total payments', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.xlabel('Terms', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.title(BASIC_PLOT_TITLE.format('% of the total payments, by term, '), fontsize=TITLE_FONT_SIZE,
               fontweight='bold')

    # display the bar
    plot.show()


def plt_days_by_term():
    """ A bar plot that groups by term information about days """

    # set a plot size
    plot.figure(figsize=PLOT_DIMENSIONS)

    # get the totals
    terms_df = roll_data.terms_overview_df()

    # plot the data
    terms_df[['Total Days', 'Days with payments', 'Days with no payments']].plot(kind='bar')

    # add labels
    plot.ylabel('Days', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.xlabel('Terms', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.title(BASIC_PLOT_TITLE.format('Number of days per term, '), fontsize=TITLE_FONT_SIZE,
               fontweight='bold')

    # display the bar
    plot.show()


def plt_business_by_term():
    """ A bar plot that groups by terms and shows number of items of business for that term. """

    # set a plot size
    plot.figure(figsize=PLOT_DIMENSIONS)

    # get the totals
    terms_df = roll_data.terms_overview_df()

    # plot the data
    ax = sns.barplot(x=terms_df.index, y=terms_df['Total entries'])

    for patch, total in zip(ax.patches, terms_df['Total entries']):
        ax.text(patch.get_x() + patch.get_width() / 2, patch.get_height(), total, ha="center",
                fontsize=ANNOTATION_FONT_SIZE, linespacing=2.0)

    # add labels
    plot.ylabel('No. of items of business', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.xlabel('Terms', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.title(BASIC_PLOT_TITLE.format('Total number of items of business, per term, '),
               fontsize=TITLE_FONT_SIZE, fontweight='bold')

    # display the bar
    plot.show()


def plt_scatter_payments_year():
    # set a plot size
    plot.figure(figsize=(10, 5))

    # get the data and remove rows with no payments
    df = roll_data.roll_with_entities_df()
    df['Date Time'] = df.apply(to_date, axis=1)
    df_plot = df[df[common.PENCE_COL] > 0]

    # create the plot
    plot.scatter(df_plot['Date Time'].tolist(), df_plot['Pence'], s=2)

    # tick range in pence (divisible by 240, which is £1)
    ticks_range = np.arange(0, 84000, 6000)

    # show the labels as £ rather than pennies
    ticks_labels = []
    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plot.yticks(ticks_range, ticks_labels)

    plot.xticks(fontsize=ANNOTATION_FONT_SIZE, rotation=90)

    # add labels
    plot.ylabel('Payment', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.xlabel('Date', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.title(BASIC_PLOT_TITLE.format('Scatter plot of all payments'), fontsize=TITLE_FONT_SIZE, fontweight='bold')

    plot.show()


def plt_all_payments():
    # set the style
    sns.set(style="darkgrid")

    plot.figure(figsize=PLOT_DIMENSIONS)
    df = roll_data.payments_overview_df()
    sns.barplot(data=df, x=common.SOURCE_COL, y=common.PENCE_COL)

    # tick range in pence (divisible by 240, which is £1)
    ticks_range = np.arange(0, 480000, 120000)

    # show the labels as £ rather than pennies
    ticks_labels = []
    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plot.yticks(ticks_range, ticks_labels)

    plot.xticks(fontsize=ANNOTATION_FONT_SIZE, rotation=90)
    plot.ylabel('Total', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.xlabel('Source', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.title(BASIC_PLOT_TITLE.format('Total payments by source'), fontsize=TITLE_FONT_SIZE, fontweight='bold')
    plot.show()


def plt_source_term_heat_map():
    """ General heat map plot """

    df = roll_data.source_term_payments_matrix_df()

    df_psd = df.applymap(money.pence_to_psd)

    plot.figure(figsize=(10, 10))
    with sns.axes_style('white'):
        hm = sns.heatmap(df, annot=df_psd, cmap='Oranges', cbar=False, fmt='', annot_kws={'size': ANNOTATION_FONT_SIZE})
        hm.set_yticklabels(hm.get_yticklabels(), rotation=0)

    plot.xlabel('Terms', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.ylabel('Source', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.title(BASIC_PLOT_TITLE.format('Payments per term by source'), fontsize=TITLE_FONT_SIZE, fontweight='bold')

    plot.show()


def plt_days_term_swarm(log=True):
    df = roll_data.roll_with_entities_df()

    # set a plot size
    plot.figure(figsize=PLOT_DIMENSIONS)

    ax = sns.stripplot(x=common.DAY_COL, y=common.PENCE_COL, hue=common.TERM_COL, data=df, jitter=0.3,
                       order=common.DAYS_OF_WEEK)
    if log:
        ax.set_ylim(bottom=1)
        ax.set_yscale('log')

    plot.xlabel('Day of the week', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.ylabel('Payment', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.title(BASIC_PLOT_TITLE.format('Payments per day'), fontsize=TITLE_FONT_SIZE, fontweight='bold')

    plot.legend(loc='lower right', shadow=True, fontsize='small')

    plot.show()


def plt_business_by_day_term(df=roll_data.roll_with_entities_df(), filter_nothing=True):
    """ A plot that shows the total number of business entered on a day and term. """

    # filter out the rows that have no receipts
    if filter_nothing:
        df = filter_out_nothing(df)

    # set the style
    sns.set(style=SN_STYLE)

    # create the plot
    sns.countplot(x=common.DAY_COL, hue=common.TERM_COL, data=df, order=common.DAYS_OF_WEEK)

    # add labels etc.
    set_labels_title('Days of the week', 'No. of items of business', 'Total no. of items occurring on a day, by term, ')

    # add a legend
    plot.legend(loc='upper center', shadow=True, fontsize='small')

    # display
    plot.show()


def plt_business_by_day(df=roll_data.roll_with_entities_df(), filter_nothing=True):
    """ A plot that shows the total number of business entered on a day. """

    # filter out the rows that have no receipts
    if filter_nothing:
        df = filter_out_nothing(df)

    # set the style
    sns.set(style=SN_STYLE)

    # create the plot
    sns.countplot(x=common.DAY_COL, data=df, order=common.DAYS_OF_WEEK)

    # Add labels etc.
    set_labels_title('Days of the week', 'No. of items of business',
                     'Total no. of items of business occurring on each day ')

    # display
    plot.show()


def plt_monthly_total():
    """ Show the monthly totals in a line plot. """

    # get the data
    df = roll_data.roll_with_entities_df()

    # set the style
    sns.set(style=SN_STYLE)

    # tick range in pence (divisible by 240, which is £1)
    ticks_range = np.arange(0, 480000, 120000)

    # show the labels as £ rather than pennies
    ticks_labels = []
    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plot.yticks(ticks_range, ticks_labels)

    # create a frequency by year, month
    df['year_month'] = df.apply(roll_data.date_to_month_year_period, axis=1)
    ax = df.groupby(df.year_month)[common.PENCE_COL].sum().plot(marker='o')
    ax.autoscale(True)

    # add labels etc.
    set_labels_title('Months', 'Total payments', 'Total payments per month ')

    plot.show()


def plt_monthly_business_count():
    """ Show the monthly counts of business in a line plot. """

    # get the data
    df = roll_data.roll_with_entities_df()

    # set the style
    sns.set(style=SN_STYLE)

    # create a frequency by year, month
    df['year_month'] = df.apply(roll_data.date_to_month_year_period, axis=1)
    ax = df.groupby(df.year_month)[common.DETAILS_COL].count().plot(marker='o')
    ax.autoscale(True)

    # add labels etc.
    set_labels_title('Months', 'Count of transactions', 'Total transactions per month ')

    plot.show()


def plt_transactions_and_totals_by_month():
    """ Plot the total count of transactions (business recorded) and the total value of that business, per month,
        as a % of the total count of transactions and the total value of business for the whole financial year. """

    # set the style
    sns.set(style=SN_STYLE)

    # get the data
    df = roll_data.transactions_and_totals_by_month()

    # plot
    ax = df.plot(marker='o')
    ax.autoscale(True)

    # add labels etc.
    set_labels_title('Months', '% of total', 'No. of transactions and their total value, \nper month, as a % of the '
                                             'total for the year')

    plot.show()


def plt_total_receipts_by_week_and_term():
    """ Create a line plot for the total value of the receipts received in each week of a term. Each term
        is plotted on its own line. """

    # set the style
    sns.set(style=SN_STYLE)

    # get data and remove 'NOTHING' values
    df = roll_data.roll_with_entities_df()
    df = filter_out_nothing(df)

    # tick range in pence (divisible by 240, which is £1)
    ticks_range = np.arange(0, 240000, 24000)

    # show the labels as £ rather than pennies
    ticks_labels = []
    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plot.yticks(ticks_range, ticks_labels)

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        values = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].sum()
        sns.lineplot(y=values, x=values.index, label=term, marker='o')

    # add labels etc.
    set_labels_title('Week', 'Total value of receipts', 'Total value of receipts for each week of the term')

    plot.show()


def plt_transaction_count_by_week_and_term():
    """ Create a line plot for number of transactions occuring each week of a term. Each term
        is plotted on its own line. """

    # set the style
    sns.set(style=SN_STYLE)

    # get data and remove 'NOTHING' values
    df = roll_data.roll_with_entities_df()
    df = df[df[common.SOURCE_COL] != 'NOTHING']

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        values = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].count()
        sns.lineplot(y=values, x=values.index, label=term, marker='o')

    # add labels etc.
    set_labels_title('Week', 'No. of transactions', 'No. of transactions for each week of the term')

    plot.show()


def plt_total_receipts_by_week_and_term_as_pc_of_year_total():
    """ Create a line plot for the total value of the receipts received in each week of a term as a percentage
        of the total receipts over the year. Each term is plotted on its own line. """

    # set the style
    sns.set(style=SN_STYLE)

    # get data and remove 'NOTHING' values
    df = roll_data.roll_with_entities_df()
    df = filter_out_nothing(df)

    # total for the year
    total = df[common.PENCE_COL].sum()

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        values = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].sum() / total * 100
        sns.lineplot(y=values, x=values.index, label=term, marker='o')

    # add labels etc.
    set_labels_title('Week', 'Value of receipts as % of year total',
                     'Total value of weekly receipts as a % of the yearly total')

    plot.show()


def plt_transactions_count_by_week_and_term_as_pc_of_year_total():
    """ Create a line plot for the total number of transactions as a percentage of the total number of transactions
        over the year. Each term is plotted on its own line. """

    # set the style
    sns.set(style=SN_STYLE)

    # get data and remove 'NOTHING' values
    df = roll_data.roll_with_entities_df()
    df = filter_out_nothing(df)

    # total for the year
    total = df[common.PENCE_COL].count()

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        values = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].count() / total * 100
        sns.lineplot(y=values, x=values.index, label=term, marker='o')

    # add labels etc.
    set_labels_title('Week', 'Value of receipts as % of year total',
                     'Number of weekly transactions as a % of the yearly total')

    plot.show()


def plt_total_receipts_by_week_and_term_as_pc_of_term_total():
    """ Create a line plot for the total value of the receipts received in each week of a term as a percentage
        of the total receipts over that term. Each term is plotted on its own line. """

    # set the style
    sns.set(style=SN_STYLE)

    # get data and remove 'NOTHING' values
    df = roll_data.roll_with_entities_df()
    df = filter_out_nothing(df)

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        # total for the year
        total = term_group[common.PENCE_COL].sum()
        values = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].sum() / total * 100
        sns.lineplot(y=values, x=values.index, label=term, marker='o')

    # add labels etc.
    set_labels_title('Week', 'Value of receipts as % of term total',
                     'Total value of weekly receipts as a % of the term total')

    plot.show()


def plt_transactions_count_by_week_and_term_as_pc_of_term_total():
    """ Create a line plot for the total number of transactions as a percentage of the total number of transactions
        over the term. Each term is plotted on its own line. """

    # set the style
    sns.set(style=SN_STYLE)

    # get data and remove 'NOTHING' values
    df = roll_data.roll_with_entities_df()
    df = filter_out_nothing(df)

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        # total for the term
        total = term_group[common.PENCE_COL].count()
        values = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].count() / total * 100
        sns.lineplot(y=values, x=values.index, label=term, marker='o')

    # add labels etc.
    set_labels_title('Week', 'Value of receipts as % of term total',
                     'Number of weekly transactions as a % of the term total')

    plot.show()


def plt_test():
    # set the style
    sns.set(style=SN_STYLE)

    # get data and remove 'NOTHING' values
    df = roll_data.roll_with_entities_df()
    df = filter_out_nothing(df)

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

        plot.show()


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
    sns.set()

    plot.figure(figsize=(8, 6))

    sns.heatmap(data, cmap=cmap, norm=norm, cbar=False)

    plot.ylabel('Months')
    plot.xlabel('Days')

    plot.yticks(rotation=0)
    plot.xticks(rotation=0)


def plt_terms_calendar():
    """ Plot that use a heatmap to show the terms against available days in a month. It illustrates the
        holidays that the Exchequer wasn't sitting. """

    cal = calendar_empty_matrix()

    # get the data
    data = roll_data.roll_with_entities_df()

    # make a pandas column of pandas Period types from the date
    data['date_period'] = data.apply(roll_data.date_to_period, axis=1)

    # populate the cal dataframe with '2' for term term dates
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
    plot.text(13, 2, 'Michaelmas')
    plot.text(13, 6, 'Hilary')
    plot.text(13, 8.6, 'Easter')
    plot.text(13, 10.6, 'Trinity')

    plot.show()


def plt_terms_calendar_payments():

    # get the data
    data = roll_data.roll_with_entities_df()

    # make a pandas column of pandas Period types from the date
    data['date_period'] = data.apply(roll_data.date_to_period, axis=1)

    # create an empty dataframe, that represents days (columns) and months (rows)
    cal = calendar_empty_matrix()

    # populate the cal dataframe with '2' for term term dates
    for term, term_period in data.groupby(common.TERM_COL, sort=False):
        term_range = pd.period_range(term_period.date_period.min(), term_period.date_period.max())
        for period in term_range:
            cal.at[period.month, period.day] = 2

    for term_day, term_group in data.groupby(data.date_period):
        if term_group[common.PENCE_COL].sum() > 0:
            cal.at[term_day.month, term_day.day] = 3

    feasts_nothing = pd.read_csv('../data/feast_nothing.csv')
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

    plot.show()
