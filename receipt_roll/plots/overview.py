"""
A collection of methods to generate plots that give an overview of the 1301-2
receipt roll data. Methods provide default arguments for titles, labels, file
names etc, but they can be overridden in case you needed to customise text
for publication.
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from receipt_roll import roll_data, money, common
from receipt_roll.plots.base import PLOT_DIMENSIONS, save_or_show, title_text, FONT_NAME, set_labels, \
    ANNOTATION_FONT_SIZE, to_date, filter_out_nothing, SN_STYLE


def plt_total_by_terms(save=True, title='Total payments, per term', x_label="Terms", y_label='Total payments',
                       is_long_title=True, file='terms_total.png', fig_size=PLOT_DIMENSIONS):
    """ A basic bar graph that shows the total payments per term.  """

    # set a plot size
    plt.figure(figsize=fig_size)

    # get the totals
    terms_df = roll_data.terms_overview_df()

    # tick range in pence (divisible by 240, which is £1)
    ticks_range = np.arange(0, 600000, 120000)

    # show the labels as £ rather than pennies
    ticks_labels = []

    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plt.yticks(ticks_range, ticks_labels, fontname=FONT_NAME)

    # plot the data
    ax = sns.barplot(x=terms_df.index, y=terms_df['Term total'])

    plt.xticks(fontname=FONT_NAME)

    # add the £.s.d. to each bar
    for patch, pence in zip(ax.patches, terms_df['Term total']):
        ax.text(patch.get_x() + patch.get_width() / 2, patch.get_height(), money.pence_to_psd(pence), ha="center",
                fontname=FONT_NAME, fontsize=ANNOTATION_FONT_SIZE, linespacing=2.0)

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)


def plt_pc_by_terms(save=True, title='% of the total payments, by term', x_label="Terms", y_label='% of total payments',
                    is_long_title=True, file='terms_total_pc.png', fig_size=PLOT_DIMENSIONS):
    """ A basic bar graph that shows the payments per term as a percentage of the whole year.  """

    # set a plot size
    plt.figure(figsize=fig_size)

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
                fontname=FONT_NAME, fontsize=ANNOTATION_FONT_SIZE, linespacing=2.0)
    plt.xticks(fontname=FONT_NAME)

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)


def plt_days_by_term(save=True, title='Number of days, per term', x_label="Terms", y_label="Days", is_long_title=False,
                     file='terms_days.png', fig_size=PLOT_DIMENSIONS):
    """ A bar plot that groups by term with information about days. """

    # set a plot size
    plt.figure(figsize=fig_size)

    # get the totals
    terms_df = roll_data.terms_overview_df()

    # plot the data
    terms_df[['Total Days', 'Days with payments', 'Days with no payments']].plot(kind='bar', colormap='tab20b')

    plt.xticks(fontname=FONT_NAME)
    plt.yticks(fontname=FONT_NAME)

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)


def plt_business_by_term(save=True, title='Total number of items of business, per term', x_label="Terms",
                         y_label="No. of items of business", is_long_title=False, file='business_by_term.png',
                         fig_size=PLOT_DIMENSIONS):
    """ A bar plot that groups by terms and shows number of items of business (profferings) for that term. """

    # set a plot size
    plt.figure(figsize=fig_size)

    # get the totals
    terms_df = roll_data.terms_overview_df()

    # plot the data
    ax = sns.barplot(x=terms_df.index, y=terms_df['Total entries'])

    for patch, total in zip(ax.patches, terms_df['Total entries']):
        ax.text(patch.get_x() + patch.get_width() / 2, patch.get_height(), total, ha="center",
                fontname=FONT_NAME, fontsize=ANNOTATION_FONT_SIZE, linespacing=2.0)

    plt.xticks(fontname=FONT_NAME)
    plt.yticks(fontname=FONT_NAME)

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)


def plt_scatter_payments_year(save=True, title='Scatter plot of all payments', x_label="Date",
                              y_label="Payment", is_long_title=False, file='scatter_plot_all_payments.png',
                              fig_size=PLOT_DIMENSIONS):
    """ A scatter plot of payments across the year. """

    # set a plot size
    plt.figure(figsize=fig_size)

    # get the data and remove rows with no payments
    df = roll_data.roll_with_entities_df()
    df['Date Time'] = df.apply(to_date, axis=1)
    df_plot = df[df[common.PENCE_COL] > 0]

    # create the plot
    plt.scatter(df_plot['Date Time'].tolist(), df_plot['Pence'], s=2)

    # tick range in pence (divisible by 240, which is £1)
    ticks_range = np.arange(0, 84000, 6000)

    # show the labels as £ rather than pennies
    ticks_labels = []
    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plt.yticks(ticks_range, ticks_labels)

    plt.xticks(fontsize=ANNOTATION_FONT_SIZE, rotation=90, fontname=FONT_NAME)

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)


def plt_total_payments_by_source(save=True, title='Total payments by source',
                                 x_label="Terms", y_label="Source", is_long_title=False,
                                 file='total_payments_source.png', fig_size=PLOT_DIMENSIONS):
    """ Bar plots showing the total amount received from each 'Source'. """

    # set the style
    sns.set(style="darkgrid")

    plt.figure(figsize=fig_size)
    df = roll_data.payments_overview_df()

    sns.barplot(data=df, x=common.SOURCE_COL, y=common.PENCE_COL)

    # tick range in pence (divisible by 240, which is £1)
    ticks_range = np.arange(0, 480000, 120000)

    # show the labels as £ rather than pennies
    ticks_labels = []
    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plt.yticks(ticks_range, ticks_labels)

    plt.xticks(fontsize=ANNOTATION_FONT_SIZE, fontname=FONT_NAME, rotation=90)

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)


def plt_source_term_heat_map(save=True, title='Payments per term by source',
                             x_label="Total", y_label="Source", is_long_title=False,
                             file='total_payments_source_heatmap.png', fig_size=(10, 10)):
    """ General heat map plot that shows the source of payments and the total values. """

    df = roll_data.source_term_payments_matrix_df()

    df_psd = df.applymap(money.pence_to_psd)

    plt.figure(figsize=fig_size)
    plt.rcParams['font.family'] = FONT_NAME
    with sns.axes_style('white'):
        hm = sns.heatmap(df, annot=df_psd, cmap='Oranges', cbar=False, fmt='', annot_kws={'size': ANNOTATION_FONT_SIZE})
        hm.set_yticklabels(hm.get_yticklabels(), rotation=0)

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)


def plt_payments_days_swarm(save=True, title='Payments per day', x_label="Day of the week", y_label="Payment",
                            is_long_title=False, file='payments_day_swarm.png', fig_size=PLOT_DIMENSIONS, log=True):
    """ Swarm plot showing the distribution of payments for each day. Each term has a different color."""

    df = roll_data.roll_with_entities_df()

    # set a plot size
    plt.figure(figsize=fig_size)

    ax = sns.stripplot(x=common.DAY_COL, y=common.PENCE_COL, hue=common.TERM_COL, data=df, jitter=0.3,
                       order=common.DAYS_OF_WEEK)
    if log:
        ax.set_ylim(bottom=1)
        ax.set_yscale('log')

    plt.legend(loc='lower right', shadow=True, fontsize='small')

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)


def plt_business_by_day_term(save=True, title='Total no. of items occurring on a day, by term',
                             x_label="Days of the week", y_label="No. of items of business",
                             is_long_title=False, file='business_day_term.png', fig_size=PLOT_DIMENSIONS,
                             filter_nothing=True):
    """ A plot that shows the total number of business entered on a day and term. """

    df = roll_data.roll_with_entities_df()

    # filter out the rows that have no receipts
    if filter_nothing:
        df = filter_out_nothing(df)

    plt.figure(figsize=fig_size)

    # set the style
    sns.set(style=SN_STYLE, font=FONT_NAME)

    # create the plot
    sns.countplot(x=common.DAY_COL, hue=common.TERM_COL, data=df, order=common.DAYS_OF_WEEK)

    # add a legend
    plt.legend(loc='upper center', shadow=True, fontsize='small')

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)


def plt_business_by_day(save=True, title='Total no. of items of business occurring on each day',
                        x_label="Days of the week", y_label="No. of items of business", is_long_title=False,
                        file='business_by_day.png', fig_size=PLOT_DIMENSIONS, filter_nothing=True):
    """ A plot that shows the total number of business entered on a day. """

    df = roll_data.roll_with_entities_df()

    # filter out the rows that have no receipts
    if filter_nothing:
        df = filter_out_nothing(df)

    plt.figure(figsize=fig_size)

    # set the style
    sns.set(style=SN_STYLE, font=FONT_NAME)

    # create the plot
    sns.countplot(x=common.DAY_COL, data=df, order=common.DAYS_OF_WEEK)

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)


def plt_receipts_week_term_as_pc_term_total(save=True, title='Total value of weekly receipts as a % of the term total',
                                            x_label="Week", y_label="Value of receipts as % of term total",
                                            is_long_title=False, file='receipts_weekly_term_pc.png',
                                            fig_size=PLOT_DIMENSIONS):
    """ Create a line plot for the total value of the receipts received in each week of a term as a percentage
        of the total receipts over that term. Each term is plotted on its own line. """

    # set the style
    sns.set(style=SN_STYLE, font=FONT_NAME)

    # get data and remove 'NOTHING' values
    df = roll_data.roll_with_entities_df()
    df = filter_out_nothing(df)

    plt.figure(figsize=fig_size)

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        # total for the year
        total = term_group[common.PENCE_COL].sum()
        values = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].sum() / total * 100
        sns.lineplot(y=values, x=values.index, label=term, marker='o')

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)


def plt_trans_count_week_term_pc_term_total(save=True, title='Number of weekly transactions as a % of the term total',
                                            x_label="Week", y_label="Value of receipts as % of term total",
                                            is_long_title=False, file='receipts_weekly_term_pc.png',
                                            fig_size=PLOT_DIMENSIONS):
    """ Create a line plot for the total number of transactions as a percentage of the total number of transactions
        over the term. Each term is plotted on its own line. """

    # set the style
    sns.set(style=SN_STYLE, font=FONT_NAME)

    # get data and remove 'NOTHING' values
    df = roll_data.roll_with_entities_df()
    df = filter_out_nothing(df)

    plt.figure(figsize=fig_size)

    for term, term_group in df.groupby(common.TERM_COL, sort=False):
        # total for the term
        total = term_group[common.PENCE_COL].count()
        values = term_group.groupby(common.WEEK_COL)[common.PENCE_COL].count() / total * 100
        sns.lineplot(y=values, x=values.index, label=term, marker='o')

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)
