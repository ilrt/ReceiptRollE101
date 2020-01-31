import numpy as np
import matplotlib.pyplot as plot
import seaborn as sn
from receipt_roll import roll_data, money


def plt_total_by_terms():
    """ A basic bar graph that shows the payments by term.  """

    # set a plot size
    plot.figure(figsize=(10, 8))

    # get the totals
    total_terms = roll_data.total_by_terms_df()

    # tick range in pence (divisible by 240, which is £1)
    ticks_range = np.arange(0, 600000, 120000)

    # show the labels as £ rather than pennies
    ticks_labels = []
    for x in np.nditer(ticks_range.T):
        ticks_labels.append(money.pence_to_psd(x))
    plot.yticks(ticks_range, ticks_labels)

    # plot the data
    ax = sn.barplot(x=total_terms.index, y=total_terms['Term total'])

    # add the £.s.d. to each bar
    for patch, pence in zip(ax.patches, total_terms['Term total']):
        ax.text(patch.get_x() + patch.get_width() / 2, patch.get_height(), money.pence_to_psd(pence), ha="center",
                fontsize=14, linespacing=2.0)

        # add labels
        plot.ylabel('Total payments', fontsize=14, fontweight='bold')
        plot.xlabel('Terms', fontsize=14, fontweight='bold')
        plot.title('Total payments, per term, in the 1301–2 receipt roll of the Irish Exchequer \n (TNA, E 101/233/16)',
                   fontsize=16, fontweight='bold')

    # display the bar
    plot.show()


def plt_pc_by_terms():
    """ A basic bar graph that shows the payments by term.  """

    # set a plot size
    plot.figure(figsize=(10, 8))

    # get the totals
    total_terms = roll_data.total_by_terms_df()

    # plot the data
    ax = sn.barplot(x=total_terms.index, y=total_terms['Term % of total'])

    # add the £.s.d. to each bar
    for patch, pc in zip(ax.patches, total_terms['Term % of total']):
        ax.text(patch.get_x() + patch.get_width() / 2, patch.get_height(), '{0:.1f}%'.format(pc), ha="center",
                fontsize=14, linespacing=2.0)

        # add labels
        plot.ylabel('% of total payments', fontsize=14, fontweight='bold')
        plot.xlabel('Terms', fontsize=14, fontweight='bold')
        plot.title('% of the total payments, by term, in the 1301–2 receipt roll \n of the Irish Exchequer (TNA, '
                   'E 101/233/16)', fontsize=16, fontweight='bold')

    # display the bar
    plot.show()
