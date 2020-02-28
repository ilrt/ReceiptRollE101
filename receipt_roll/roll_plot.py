from datetime import datetime

import numpy as np
import matplotlib.pyplot as plot
import seaborn as sn
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
    ax = sn.barplot(x=terms_df.index, y=terms_df['Term total'])

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
    ax = sn.barplot(x=term_total_as_pc.index, y=term_total_as_pc)

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
    ax = sn.barplot(x=terms_df.index, y=terms_df['Total entries'])

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
    sn.set(style="darkgrid")

    plot.figure(figsize=PLOT_DIMENSIONS)
    df = roll_data.payments_overview_df()
    sn.barplot(data=df, x=common.SOURCE_COL, y=common.PENCE_COL)

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
    with sn.axes_style('white'):
        hm = sn.heatmap(df, annot=df_psd, cmap='Oranges', cbar=False, fmt='', annot_kws={'size': ANNOTATION_FONT_SIZE})
        hm.set_yticklabels(hm.get_yticklabels(), rotation=0)

    plot.xlabel('Terms', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.ylabel('Source', fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plot.title(BASIC_PLOT_TITLE.format('Payments per term by source'), fontsize=TITLE_FONT_SIZE, fontweight='bold')

    plot.show()


def plt_days_term_swarm(log=True):
    df = roll_data.roll_with_entities_df()

    # set a plot size
    plot.figure(figsize=PLOT_DIMENSIONS)

    ax = sn.stripplot(x=common.DAY_COL, y=common.PENCE_COL, hue=common.TERM_COL, data=df, jitter=0.3,
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
    sn.set(style=SN_STYLE)

    # create the plot
    sn.countplot(x=common.DAY_COL, hue=common.TERM_COL, data=df, order=common.DAYS_OF_WEEK)

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
    sn.set(style=SN_STYLE)

    # create the plot
    sn.countplot(x=common.DAY_COL, data=df, order=common.DAYS_OF_WEEK)

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
    sn.set(style=SN_STYLE)

    # tick range in pence (divisible by 240, which is £1)
    ticks_range = np.arange(0, 480000, 120000)

    # show the labels as £ rather than pennies
    ticks_labels = []
    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plot.yticks(ticks_range, ticks_labels)

    # create a frequency by year, month
    df['year_month'] = df.apply(roll_data.date_to_month_year_period, axis=1)
    df.groupby(df.year_month)[common.PENCE_COL].sum().plot()

    # add labels etc.
    set_labels_title('Months', 'Total payments', 'Total payments per month ')

    plot.show()


def plt_monthly_business_count():
    """ Show the monthly counts of business in a line plot. """

    # get the data
    df = roll_data.roll_with_entities_df()

    # set the style
    sn.set(style=SN_STYLE)

    # create a frequency by year, month
    df['year_month'] = df.apply(roll_data.date_to_month_year_period, axis=1)
    df.groupby(df.year_month)[common.DETAILS_COL].count().plot()

    # add labels etc.
    set_labels_title('Months', 'Count of transactions', 'Total transactions per month ')

    plot.show()
