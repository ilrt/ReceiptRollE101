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


def to_date(row):
    return datetime.strptime(str(row['Date']), '%Y-%m-%d')


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


def plt_scatter_payments_year():
    # set a plot size
    plot.figure(figsize=PLOT_DIMENSIONS)

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
