import pandas as pd
from receipt_roll import roll_data, common
import numpy as np
import matplotlib.pyplot as plt
from math import pi


def plt_terms_business_radar():
    """ Create four radar charts that show the relationship, for each term, between the length of the term,
        the amount of business (transactions) and total amount of receipts. """

    # get the data
    df = roll_data.roll_with_entities_df()

    # create an empty dataframe to hold the summary data
    categories = ['Days', 'Transactions', 'Income']
    radar_df = pd.DataFrame(np.zeros(shape=(len(categories), len(common.TERMS))),
                            columns=common.TERMS, index=categories)

    # ----- Length of the terms (as a % of the total)

    # temp structure to track the start and end dates of each term
    days = {}

    # create a Period from the date
    df['Period'] = df.apply(roll_data.date_to_period, axis=1)

    # get the  start and end dates for each term
    for term, term_group in df.groupby(common.TERM_COL):
        start_day = term_group['Period'].min()
        end_day = term_group['Period'].max()
        period_range = pd.period_range(start_day, end_day)
        days[term] = len(period_range)

    # total amount of days
    total_terms_days = sum(days.values())

    # update the radar dataframe with the % values
    for key in days.keys():
        radar_df.at['Days', key] = days[key] / total_terms_days * 100

    # ----- Number of transactions (as a % of the total)

    # total transaction over the year
    total_transactions = df[common.PENCE_COL].count()

    # transactions as a % added to the radar dataframe
    for term, term_group in df.groupby(common.TERM_COL):
        terms_transaction = term_group[common.PENCE_COL].count()
        radar_df.at['Transactions', term] = terms_transaction / total_transactions * 100

    # ----- Value of transactions (as a % of the total)

    # total amount received
    total_payments = df[common.PENCE_COL].sum()

    # amount as a % added to the radar dataframe
    for term, term_group in df.groupby(common.TERM_COL):
        terms_payments = term_group[common.PENCE_COL].sum()
        radar_df.at['Income', term] = terms_payments / total_payments * 100

    # colours to use in the plots (one for each term)
    colours = ['#F06292', '#FFB74D', '#64B5F6', '#81C784']

    # create a chart for each term
    for idx, term in enumerate(common.TERMS):
        values = radar_df.loc[:, term].values.flatten().tolist()
        plot_radar(categories, values, term, colours[idx])


def plot_radar(categories, values, title, colour):
    """ Provide a radar chart. This borrows heavily from https://python-graph-gallery.com/390-basic-radar-chart/"""
    n = len(categories)

    values += values[:1]

    angles = [x / float(n) * 2 * pi for x in range(n)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='black', size=8)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([10, 20, 30, 40], ["10", "20", "30", "40"], color="black", size=7)
    plt.ylim(0, 50)

    # Plot data
    ax.plot(angles, values, linewidth=2, linestyle='solid')

    # Fill area
    ax.fill(angles, values, colour, alpha=0.1)

    plt.title(title)

    plt.show()
