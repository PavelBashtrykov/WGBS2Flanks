from matplotlib import pyplot as plt
from numpy import float64

import seaborn as sns
import pandas as pd
from utils.data import FlanksData


class SimpleBarplot:
    def plot(self, sample: FlanksData, reference: FlanksData):
        sample.data["sample"] = "control"
        reference.data["sample"] = "reference"
        df = pd.concat([sample.data, reference.data], axis=0, ignore_index=True)
        cols = ["Av. mC"]
        # df2.set_axis(cols, axis=1,inplace=True)
        df[cols] = df[cols].astype(float64)
        plt.close("all")
        fig, ax = plt.subplots(figsize=(6,8))
        sns.set_theme(style="whitegrid")
        palette = sns.color_palette("Paired") # ("Blues", 9)
        ax = sns.barplot(
            data=df,
            x='Site',
            y="Av. mC",
            hue="sample",
            # color=palette[2], 
            edgecolor="white", # palette[3],
            linewidth=1
        )
        ax.set_xlabel("Flanks")
        ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
        ax.set_ylabel("Methylation")
        ax.set_title("Methylation of various flanks",
            fontsize=14,
            color="black", # palette[3]
            fontweight="normal", #'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight'
            )
        ax.set_ylim(0.7,.9)
        sns.despine()
        plt.savefig("simple_bar_plot.png", dpi=200)