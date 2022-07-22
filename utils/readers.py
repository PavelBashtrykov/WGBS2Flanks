#! /usr/bin/env python3.10
################################################################################
# This script is written by Pavel Bashtrykov
# pavel.bashtrykov@ibtb.uni-stuttgart.de
# pavel.bashtrykov@gmail.com
################################################################################

from matplotlib.pyplot import table
import pandas as pd
from typing import Protocol

from utils.data import ComputeFlanksDataStorage, FlanksData, ReferenceFlanksStorage, Storage


class Reader(Protocol):
    """Interfase for reading input files of different formats"""
    def read(self, infile) -> Storage:
        ...


class AlbertsFlanksReader:
    """Reads data from csv file produced by Albert's script"""
    def read(self, infile) -> ComputeFlanksDataStorage:
        st = ComputeFlanksDataStorage(file_name=infile)
        with open(infile, "r") as fh:
            blocks = _split_albert_flanks_csv(fh)
            for ind, block in enumerate(blocks):
                fd = FlanksData(ind+1, block)
                st.add(fd)
        return st


class ComputeFlanksCSVReader:
    """Reads data from a csv file produced by computeFlanks.py"""
    def read(self, infile) -> ComputeFlanksDataStorage:
        st = ComputeFlanksDataStorage(file_name=infile)
        with open(infile, "r") as fh:
            blocks = _split_compute_flanks_csv(fh)
            for ind, block in enumerate(blocks):
                fd = FlanksData(ind+1, block)
                st.add(fd)
        return st


class PreferenceFileCSVReader:
    """Reads data from a csv file containing reference flaking data"""
    def read(self, infile) -> ReferenceFlanksStorage:
        st = ReferenceFlanksStorage(file_name=infile)
        with open(infile, "r") as fh:
            st.add(_read_ref_flanks_to_df(fh))
            return st

def read_input(infile, reader: Reader) -> Storage:
    return reader.read(infile)

def _split_albert_flanks_csv(fileholder) -> list[pd.DataFrame]:
    blocks = []
    column_names = None
    temp_storage = []
    
    line = fileholder.readline()
    while line:
        if line.startswith("Site"): # get column names
                column_names = line.strip().strip(",").split(",")
                line = fileholder.readline()
        elif line.startswith(",") and column_names: # end of the block with ",,," line
            df = pd.DataFrame(temp_storage)
            df.columns = column_names
            blocks.append(df)
            # "empty" variables
            column_names = None
            temp_storage = []
            line = fileholder.readline()
        elif line.strip()=="" and column_names: # end of the block with empty line
            df = pd.DataFrame(temp_storage)
            df.columns = column_names
            blocks.append(df)
            # "empty" variables
            column_names = None
            temp_storage = []
            line = fileholder.readline()
        elif line.startswith(",") and not column_names:
            line = fileholder.readline()
        else:
            d = line.strip().strip(",").split(",")
            temp_storage.append(d)
            line = fileholder.readline()
    df = pd.DataFrame(temp_storage)
    df.columns = column_names  # type: ignore
    blocks.append(df)

    return blocks

def _split_compute_flanks_csv(fileholder) -> list[pd.DataFrame]:
    blocks = []
    column_names = None
    temp_storage = []
    
    line = fileholder.readline()
    while line:
        if line.startswith("Site"): # get column names
                column_names = line.strip().split(";")
                line = fileholder.readline()
        elif line.startswith(",") and column_names: # end of the block with ",,," line
            df = pd.DataFrame(temp_storage)
            df.columns = column_names
            blocks.append(df)
            # "empty" variables
            column_names = None
            temp_storage = []
            line = fileholder.readline()
        elif line.strip()=="" and column_names: # end of the block with empty line
            df = pd.DataFrame(temp_storage)
            df.columns = column_names
            blocks.append(df)
            # "empty" variables
            column_names = None
            temp_storage = []
            line = fileholder.readline()
        elif line.startswith(",") and not column_names:
            line = fileholder.readline()
        else:
            d = line.strip().split(";")
            temp_storage.append(d)
            line = fileholder.readline()

    return blocks

def _read_ref_flanks_to_df(fileholder) -> list[pd.DataFrame]:
    df = pd.read_csv(fileholder, sep=";")
    return df