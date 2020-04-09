import matplotlib.pyplot as plt
from math import pi

from receipt_roll.plots.base import save_or_show


def plot_radar(categories, values, title, colour, save=False, file_name='radar.png', file_format='png'):
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

    save_or_show(save, file_name, file_format)
