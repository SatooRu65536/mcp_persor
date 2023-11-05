import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib


def plot(
    df,
    heads,
    title,
    xlabel,
    ylabel,
    figsize=(10, 3),
    xlim=(0, 0),
    ylim=(0, 0),
    grid=True,
):
    fig = plt.figure(figsize=figsize)

    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if grid:
        plt.grid(color='k', linestyle='dotted', linewidth=1, alpha=0.5)

    if xlim[0] < xlim[1]:
        plt.xlim(xlim[0], xlim[1])
        if xgap > 0:
            plt.xticks(np.arange(int(xlim[0]), int(xlim[1]), xgap))

    if ylim[0] < ylim[1]:
        plt.ylim(ylim[0], ylim[1])
        if ygap > 0:
            plt.yticks(np.arange(int(ylim[0]), int(ylim[1]), ygap))

    for head in heads:
        plt.plot(df[head[0]], df[head[1]], label=head[1])

    plt.legend()
    plt.show()
