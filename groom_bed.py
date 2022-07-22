#! /usr/bin/env python
################################################################################
# This script is written by Pavel Bashtrykov
# pavel.bashtrykov@ibtb.uni-stuttgart.de
# pavel.bashtrykov@gmail.com
################################################################################


import argparse


def _convert(file):

    # another version using pandas, eats lots of memory

    # import pandas as pd

    # df = pd.read_csv(file, sep="\t", header=None)
    # df[["meth","coor"]] = df[0].str.split("::", expand=True)
    # df.drop([0], axis=1, inplace=True)
    # df[["chr","coor2"]] = df["coor"].str.split(":", expand=True)
    # df.drop(["coor"], axis=1, inplace=True)
    # df[["coor3","strand"]] = df["coor2"].str.split("(", expand=True)
    # df.drop(["coor2"], axis=1, inplace=True)
    # df["strand"] = df["strand"].str.strip(")")
    # df[["start", "end"]] = df["coor3"].str.split("-",expand=True)
    # df.drop(["coor3"], axis=1, inplace=True)#
    # df["name"] = df[1] + ":" + df["meth"]
    # df.drop([1,"meth"], axis=1, inplace=True)
    # df["score"] = ""
    # df = df[["chr", "start", "end", "name", "score", "strand"]]

    # new_file = file.strip("txt") + ".bed6.bed"

    # df.to_csv(new_file, header=None, index=None, sep='\t', mode='w')

    with open(file, "r") as fh, open(file.rstrip("txt")+"bed6.bed", "w") as sh:
        for line in fh:
            tag, sequence = line.strip().split("\t")
            meth, coor = tag.split("::")
            name = sequence + ":" + meth
            chr, rest = coor.split(":")
            coor2, strand_temp = rest.split("(")
            start, end = coor2.split("-")
            strand = strand_temp.strip(")")
            sh.write("\t".join([chr,start, end, name, "", strand+"\n"]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", help="Provide an input file (produced by bedtools getfasta)", type=str, required=True)
    args = parser.parse_args()

    file = args.infile
    _convert(file)


if __name__ == "__main__":
    main()