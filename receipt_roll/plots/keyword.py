import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from nltk import FreqDist

from receipt_roll import roll_data, common
from receipt_roll.plots.base import save_or_show, set_labels, title_text, SN_STYLE, FONT_NAME, PLOT_DIMENSIONS


def plt_keyword_frequency(title='{} most frequent keywords', x_label='Keyword', y_label='Frequency', limit=20,
                          save=False, is_long_title=False, file='plt_keyword_frequency.png', fig_size=PLOT_DIMENSIONS):
    """" Display a plot that shows the most frequent keywords. The number of words is determined by the limit. """

    # set the style
    sns.set(style=SN_STYLE, font=FONT_NAME)

    plt.figure(figsize=fig_size)

    title = title.format(limit)

    # get data
    df = roll_data.roll_with_entities_df()

    # filter out rows without keywords
    df_keywords = df[df[common.KEYWORDS_COL].notnull()]

    # get keywords as a list
    all_keywords = df_keywords[common.KEYWORDS_COL].to_list()

    # remove the semicolon delimiter
    kw = []
    for k in all_keywords:
        for i in k.split(';'):
            kw.append(i)

    kw_freq = FreqDist(kw)

    # create a pandas as df
    kw_df = pd.DataFrame(kw_freq.most_common(limit), columns=['Word', 'Frequency']).set_index('Word')

    sns.set()

    kw_df.plot(kind='bar', legend=None)
    plt.xticks(fontsize=10, fontname=FONT_NAME)
    plt.yticks(fontsize=10, fontname=FONT_NAME)

    # plot labels
    set_labels(x_label, y_label)

    # plot title
    title_text(title, is_long_title)

    # show or save the image to file
    save_or_show(save=save, plot_file_name=file)
