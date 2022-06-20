#! /usr/bin/env python3.10
################################################################################
# This script is written by Pavel Bashtrykov
# pavel.bashtrykov@ibtb.uni-stuttgart.de
# pavel.bashtrykov@gmail.com
################################################################################

from typing import Protocol

from utils.data import FlanksData


class PlotMaker(Protocol):
    def plot(self, sample: FlanksData, reference: FlanksData):
        ...

def make_plot(sample: FlanksData, reference: FlanksData, plotmaker: PlotMaker):
    plotmaker.plot(sample, reference)