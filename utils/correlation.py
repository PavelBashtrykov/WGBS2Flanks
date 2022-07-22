#! /usr/bin/env python3.10
################################################################################
# This script is written by Pavel Bashtrykov
# pavel.bashtrykov@ibtb.uni-stuttgart.de
# pavel.bashtrykov@gmail.com
################################################################################

from typing import Protocol

from utils.data import Storage


class Correlation(Protocol):
    def corr(self, sample: Storage, reference: Storage):
        ...

def make_plot(sample: Storage, reference: Storage, plotmaker: Correlation):
    plotmaker.corr(sample, reference)