from receipt_roll import common
from receipt_roll.data import roll
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

from receipt_roll.plots.base import set_labels_title, save_or_show


def df_sheriffs():
    df = roll.roll_with_entities_df()
    df['month_year'] = df.apply(roll.date_to_month_year_period, axis=1)
    sheriffs_df = df[df[common.PEOPLE_COL].notnull() & df[common.PEOPLE_COL].str.contains('sheriff')]
    # error in data, remove Dublin Manor
    return sheriffs_df[sheriffs_df[common.SOURCE_COL] != 'DUBLIN MANOR']


def plt_sheriffs_counties_terms_heatmap(save=False, file_name='plt_sheriffs_counties_terms_heatmap.png',
                                        file_format='png'):
    # just get the sheriffs
    df = df_sheriffs()

    # counties
    counties = list(set(df[common.SOURCE_COL].to_list()))
    counties.sort()

    matrix = pd.DataFrame(np.zeros(shape=(len(counties), len(common.TERMS))), columns=common.TERMS, index=counties)
    for term, term_group in df.groupby(common.TERM_COL):
        for area, area_group in term_group.groupby(common.SOURCE_COL):
            matrix.at[area, term] = 1

    cmap = mpl.colors.ListedColormap(['#ffffff', '#c28cb8'])
    norm = mpl.colors.BoundaryNorm([0, 1, 3], cmap.N)
    sns.heatmap(matrix, cmap=cmap, norm=norm, cbar=False)

    # add labels etc.
    set_labels_title('Terms', 'Shires',
                     'Terms that sheriffs appeared')

    save_or_show(save, file_name, file_format)


def plt_sheriffs_counties_terms_no_arrears_heatmap(save=False,
                                                   file_name='plt_sheriffs_counties_terms_no_arrears_heatmap.png',
                                                   file_format='png'):
    # just get the sheriffs
    df = df_sheriffs()

    df = df[~df[common.DETAILS_COL].str.contains('arrears')]

    # counties
    counties = list(set(df[common.SOURCE_COL].to_list()))
    counties.sort()

    matrix = pd.DataFrame(np.zeros(shape=(len(counties), len(common.TERMS))), columns=common.TERMS, index=counties)
    for term, term_group in df.groupby(common.TERM_COL):
        for area, area_group in term_group.groupby(common.SOURCE_COL):
            matrix.at[area, term] = 1

    cmap = mpl.colors.ListedColormap(['#ffffff', '#c28cb8'])
    norm = mpl.colors.BoundaryNorm([0, 1, 3], cmap.N)
    sns.heatmap(matrix, cmap=cmap, norm=norm, cbar=False)

    # add labels etc.
    set_labels_title('Terms', 'Shires',
                     'Terms that sheriffs appeared (arrears removed)')

    save_or_show(save, file_name, file_format)


def plt_sheriffs_counties_month_heatmap(save=False, file_name='plt_sheriffs_counties_month_heatmap.png',
                                        file_format='png'):
    # just get the sheriffs
    df = df_sheriffs()

    # months
    months = list(set(df.month_year.to_list()))
    months.sort()

    # counties
    counties = list(set(df[common.SOURCE_COL].to_list()))
    counties.sort()

    matrix = pd.DataFrame(np.zeros(shape=(len(counties), len(months))), columns=months, index=counties)
    for month, month_group in df.groupby(df.month_year):
        for area, area_group in month_group.groupby(common.SOURCE_COL):
            matrix.at[area, month] = 1

    cmap = mpl.colors.ListedColormap(['#ffffff', '#0099ff'])
    norm = mpl.colors.BoundaryNorm([0, 1, 3], cmap.N)
    sns.heatmap(matrix, cmap=cmap, norm=norm, cbar=False)

    # add labels etc.
    set_labels_title('Month', 'Shires',
                     'Months that sheriffs appeared')

    save_or_show(save, file_name, file_format)


def plt_sheriffs_counties_month_no_arrears_heatmap(save=False,
                                                   file_name='plt_sheriffs_counties_month_no_arrears_heatmap.png',
                                                   file_format='png'):
    # just get the sheriffs
    df = df_sheriffs()
    df = df[~df[common.DETAILS_COL].str.contains('arrears')]

    # months
    months = list(set(df.month_year.to_list()))
    months.sort()

    # counties
    counties = list(set(df[common.SOURCE_COL].to_list()))
    counties.sort()

    matrix = pd.DataFrame(np.zeros(shape=(len(counties), len(months))), columns=months, index=counties)
    for month, month_group in df.groupby(df.month_year):
        for area, area_group in month_group.groupby(common.SOURCE_COL):
            matrix.at[area, month] = 1

    cmap = mpl.colors.ListedColormap(['#ffffff', '#CD644E'])
    norm = mpl.colors.BoundaryNorm([0, 1, 3], cmap.N)
    sns.heatmap(matrix, cmap=cmap, norm=norm, cbar=False)

    # add labels etc.
    set_labels_title('Month', 'Shires',
                     'Months that sheriffs appeared (arrears removed)')

    save_or_show(save, file_name, file_format)


def plt_sheriffs_counties_month_arrears_heatmap():
    # just get the sheriffs
    df = df_sheriffs()

    # months
    months = list(set(df.month_year.to_list()))
    months.sort()

    # counties
    counties = list(set(df[common.SOURCE_COL].to_list()))
    counties.sort()

    df_arrears = df[df[common.KEYWORDS_COL].str.contains('arrears')]

    matrix = pd.DataFrame(np.zeros(shape=(len(counties), len(months))), columns=months, index=counties)
    for month, month_group in df_arrears.groupby(df_arrears.month_year):
        for area, area_group in month_group.groupby(common.SOURCE_COL):
            matrix.at[area, month] = 1

    cmap = mpl.colors.ListedColormap(['#ffffff', '#ff3300'])
    norm = mpl.colors.BoundaryNorm([0, 1, 3], cmap.N)
    sns.heatmap(matrix, cmap=cmap, norm=norm, cbar=False)

    plt.show()
