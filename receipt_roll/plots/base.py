import matplotlib.pyplot as plt
import os

import settings

# standard title format
BASIC_PLOT_TITLE = "{} \n in the 1301–2 receipt roll of the Irish Exchequer \n (The National Archives, London, " \
                   "E 101/233/16) "

# default plot dimensions
PLOT_DIMENSIONS = (6, 5)
TITLE_FONT_SIZE = 12
LABEL_FONT_SIZE = 10
ANNOTATION_FONT_SIZE = 8

# default Seaborn style
SN_STYLE = 'darkgrid'


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
        plt.savefig(fname=file_name, format=plt_format, bbox_inches='tight')
    else:
        plt.show()
    plt.close()
