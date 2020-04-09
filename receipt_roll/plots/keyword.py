import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from nltk import FreqDist

from receipt_roll.roll_plot import set_labels_title
from receipt_roll import roll_data, common
from receipt_roll.plots.base import save_or_show


def plt_keyword_frequency(limit=20, save=False, file_name='plt_keyword_frequency.png', file_format='png'):
    """" Display a plot that shows the most frequent keywords. The number of words is determined by the limit. """

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
    plt.xticks(fontsize=8)

    set_labels_title('Keyword', 'Frequency', '{} most frequent keywords'.format(limit))

    save_or_show(save, file_name, file_format)
