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

class SimpleHeatmapMaker:
    """One data set vs one refernce flanking preference.
    """
    def plot(self, sample: FlanksData, reference: FlanksData):
        df = sample.data.merge(reference.data, on="Site")
        df2 = df.drop(df.iloc[:,[0,1,3]], axis=1)
        cols = ["control",'experiment']
        df2.set_axis(cols, axis=1,inplace=True)
        df2[cols] = df2[cols].astype(float64)
        df2.sort_values(by="control", ascending=False, inplace=True)
        fig, ax = plt.subplots()
        ax = sns.heatmap(
            data=df2,
            yticklabels=False,
            cmap="Blues",
            ax=ax
            )
        ax.axvline([1], *ax.get_ylim(), color="w", linewidth=0.5)
        
        plt.savefig("heatmap.png", dpi=200)
