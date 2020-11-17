from datetime import datetime

import matplotlib.pyplot as plt
import os

import settings

# standard title format
from receipt_roll import common

BASIC_PLOT_TITLE = "{} \n in the 1301–2 receipt roll of the Irish Exchequer \n (The National Archives, London, " \
                   "E 101/233/16) "

# default plot dimensions
FONT_NAME = 'Times New Roman'
PLOT_DIMENSIONS = (8, 5)
TITLE_FONT_SIZE = 12
LABEL_FONT_SIZE = 10
ANNOTATION_FONT_SIZE = 10

# default Seaborn style
SN_STYLE = 'darkgrid'

# months (labels)
months_labels_cal = ['[1301] Sep', 'Oct', 'Nov', 'Dec', '[1302] Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']


def to_date(row):
    return datetime.strptime(str(row['Date']), '%Y-%m-%d')


def filter_out_nothing(df):
    """ Filter out rows where no receipts are recorded. """
    return df[df[common.SOURCE_COL] != 'NOTHING']


def title_text(plot_title, is_long=True):
    """
    Creates a title for a plot. If the title is long, it appends the roll details
    and TNA reference number to the provided title.

    :param plot_title:  title of the plot
    :param is_long:     should the TNA reference be added to the title?
    """

    if is_long:
        plot_title = BASIC_PLOT_TITLE.format(plot_title)
    plt.title(plot_title, fontname=FONT_NAME, fontsize=TITLE_FONT_SIZE, fontweight='bold')


def set_labels(x_label, y_label):
    """
    Set the x and y labels for a plot.

    :param x_label: x-axis label
    :param y_label: y-axis label
    """
    plt.xlabel(x_label, fontname=FONT_NAME, fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plt.ylabel(y_label, fontname=FONT_NAME, fontsize=LABEL_FONT_SIZE, fontweight='bold')


def set_labels_title(x_label, y_label, title):
    """ Helper text to set x and y labels and title for a plot. """

    plt.xlabel(x_label, fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plt.ylabel(y_label, fontsize=LABEL_FONT_SIZE, fontweight='bold')
    plt.title(BASIC_PLOT_TITLE.format(title), fontsize=TITLE_FONT_SIZE, fontweight='bold')


def save_or_show(save=False, plot_file_name='plot.png', plt_format='png'):
    """ Helper method that displays or saves a plot. """

    if not os.path.exists(settings.PLOT_IMG_DIR):
        os.makedirs(settings.PLOT_IMG_DIR)

    file_name = os.path.join(settings.PLOT_IMG_DIR, plot_file_name)

    if save:
        plt.savefig(fname=file_name, format=plt_format, bbox_inches='tight', dpi=300)
    else:
        plt.show()
    plt.close()
