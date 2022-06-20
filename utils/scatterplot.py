#! /usr/bin/env python3.10
################################################################################
# This script is written by Pavel Bashtrykov
# pavel.bashtrykov@ibtb.uni-stuttgart.de
# pavel.bashtrykov@gmail.com
################################################################################

from matplotlib import pyplot as plt
from numpy import float64
import seaborn as sns

from utils.data import FlanksData


class SimpleScatterplot:
    def plot(self, sample: FlanksData, reference: FlanksData):
        df = _merge_data(sample, reference)
        plt.close("all")
        # https://seaborn.pydata.org/generated/seaborn.axes_style.html#seaborn.axes_style
        custom_params = {"axes.spines.right": True, "axes.spines.top": True}
        # style: None, dict, or one of {darkgrid, whitegrid, dark, white, ticks}
        sns.set_theme(rc=custom_params)
        fig, ax = plt.subplots()
        ax = sns.scatterplot(
            data=df,
            x="control",
            y="experiment",
            s=10,
            ax=ax
            )
        #ax.set(yticklabels=[])
        #ax.set(xticklabels=[])
        #ax.set_xticks([0, .5, 1])
        ax.tick_params(left=False)
        ax.set_title('Correlation plot')
        ax.set_xlabel("Control")
        ax.set_ylabel("Treatment")
        plt.savefig("simple_scatter_plot.png", dpi=200)
    
def _merge_data(sample: FlanksData, reference: FlanksData):
        df = sample.data.merge(reference.data, on="Site")
        df2 = df.drop(df.iloc[:,[0,1,3]], axis=1)
        cols = ["control",'experiment']
        df2.set_axis(cols, axis=1, inplace=True)
        df2[cols] = df2[cols].astype(float64)
        df2.sort_values(by="control", ascending=False, inplace=True)
        return df2