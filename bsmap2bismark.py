#!/usr/bin/env python

# Converts WGBS result produced by Bsmap to bismark format

import sys


def main(infile):
    outfile = infile + ".bis.txt"
    with open(infile, "r") as fh, open(outfile, "w") as out:
        for i in fh:
            data = i.strip().split()
            coordinates = data[:2]
            watson = data[2:4]
            crick = data[4:6]
            out.write("\t".join(coordinates+ ["+"] + watson + ["NA","NA"]))
            out.write("\n")
            start = str(int(coordinates.pop()) + 1)
            coordinates.append(start)
            out.write("\t".join(coordinates+ ["-"] + crick + ["NA","NA"]))
            out.write("\n")


if __name__ == "__main__":
    main(sys.argv[1])