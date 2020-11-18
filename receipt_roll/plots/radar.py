import matplotlib.pyplot as plt
from math import pi
import numpy as np
import pandas as pd

from receipt_roll import common
from receipt_roll.data import roll
from receipt_roll.plots.base import save_or_show, ANNOTATION_FONT_SIZE, TITLE_FONT_SIZE


def plot_radar(categories, values, title, colour, save=False, file_name='radar.png', file_format='png'):
    """ Provide a radar chart. This borrows heavily from https://python-graph-gallery.com/390-basic-radar-chart/"""

    n = len(categories)

    values += values[:1]

    angles = [x / float(n) * 2 * pi for x in range(n)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, fontname="Times New Roman", color='black', size=10)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([10, 20, 30, 40], ["10", "20", "30", "40"], fontname="Times New Roman", color="black",
               size=ANNOTATION_FONT_SIZE)
    plt.ylim(0, 50)

    # Plot data
    ax.plot(angles, values, linewidth=2, linestyle='solid')

    # Fill area
    ax.fill(angles, values, colour, alpha=0.1)

    plt.title(title, fontname="Times New Roman", fontsize=TITLE_FONT_SIZE, fontweight='bold')

    save_or_show(save, file_name, file_format)


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
    fig_num = 4
    for idx, term in enumerate(common.TERMS):
        values = radar_df.loc[:, term].values.flatten().tolist()
        plt_file_name = "{}_{}_{}".format(fig_num, term.lower(), file_name)
        plot_radar(categories, values, "{}. {}".format(fig_num, term), colours[idx], save, plt_file_name, file_format)
        fig_num = fig_num + 1
