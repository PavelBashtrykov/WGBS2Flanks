#! /usr/bin/env python
################################################################################
# This script is written by Pavel Bashtrykov
# pavel.bashtrykov@ibtb.uni-stuttgart.de
# pavel.bashtrykov@gmail.com
################################################################################

import argparse
from itertools import product
from collections import OrderedDict


def main():
    # paramethers of the run
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", help="Input file", type=str, required=True)
    parser.add_argument("-o", "--outfile", help="Output file", type=str)
    parser.add_argument(
        "-d",
        "--depth",
        help="Define a minimum sequencing depth for cytosines to be included into analysis",
        required=False,
    )
    parser.add_argument("-m", "--motif", help="Sequence motif, default: CG", type=str, required=False)
    args = parser.parse_args()

    infile = args.infile
    savein = (
        args.outfile if args.outfile else infile + "_flanks_methylation.csv"
    )  # default name for outfile
    seq_depth = (
        int(args.depth) if args.depth else 10
    )  # default value of sequencing depth
    print(f"Depth limit is {seq_depth}")
    seq_motif = args.motif if args.motif else "CG"
    print(f"Motif: {seq_motif}")

    # main part
    for flank_size in range(1, 4):
        empty_flanks_dict = _make_flanks_dict(flank_size, motif=seq_motif)
        if seq_depth==0:
            flanks_stat = _compute_flanks_frequencies(flank_size, empty_flanks_dict, infile, motif=seq_motif)
        else:
            # flanks_stat = _compute_flanks_methylation(flank_size, empty_flanks_dict, infile, seq_depth, motif=seq_motif)
            flanks_stat = _compute_flanks_methylation_proper_bed(flank_size, empty_flanks_dict, infile, seq_depth, motif=seq_motif)
        
        _save_data(flanks_stat, savein)
        print(f"Flank {flank_size} is done")

def _make_flanks_dict(flank_size: int, motif: str = "CG") -> OrderedDict[str, list]:
    """
    Make a dictionary of flanks

    Parameters
    ----------
    flank_size : int, number of nucleotides flanking CG to analyse (max 3).
        E.g. if flank_size=1 then flank is NCGN
    
    motif : str, central motif.
        E.g. CG, CA, etc., default = "CG"

    Returns
    -------
    flnak_dict : dictionary, all flanks with [0,0] [counts of Cs with this flank, sum of methylation levels]
        {"ACGA": [0,0],
        "ACGT": [0,0],
        ..............,
        "CCGC": [0,0]
        }
        
    """
    # generate empty dictionaries with e.g. NCGN flanks
    letters = "ACGT"
    flanks_list = ["".join(x) for x in list(product(letters, repeat=flank_size * 2))]
    flanks_dict = OrderedDict()
    for f in flanks_list:
        sequence = f[:flank_size] + motif + f[flank_size:]
        flanks_dict[sequence] = [0, 0]  # [counts, sum of methylation levels]
    return flanks_dict

def _compute_flanks_methylation(
    flank_size: int, flank_dict: OrderedDict, infile: str, depth_limit: int = 10, motif: str = "CG"
):
    """Computes methylation of flanks
    
    Parameters
    ----------

    flank_size : int, number of nucleotides flanking CN to analyse (max 3)
    flank_dict : dict, disctionary of flanks to store statistics
    infile : str, input file with sequences and methylation data
    depth_limit : int, sets a treshold for sequencing depth, default = 10,
        a minimum number of sequencing depth to take cytosine into analysis
    
    Returns
    -------

    flank_dict : dict, dictionary of flanks and methylation statistics
    """
    seq_start = int(22 / 2 - len(motif) / 2 - flank_size)
    seq_end = int(22 / 2 + len(motif) / 2 + flank_size)
    
    with open(infile, "r") as fh:
        data = fh.readlines()
        for line in data:
            header, sequence = line.split()
            header_splited = header.split(":")[0].split(";")
            mC, total = header_splited[0], header_splited[1]
            depth = int(total)
            if depth >= depth_limit:
                flank = sequence.upper()[seq_start:seq_end]
                if flank in flank_dict.keys():
                    meth_level = int(mC) / depth  # methylation level
                    flank_dict[flank][0] += 1  # increament count
                    flank_dict[flank][
                        1
                    ] += meth_level  # add methylation level to compute average at the end

    # compute average methylation
    for key, value in flank_dict.items():
        if value[0] > 0:
            flank_dict[key][1] = value[1] / value[0]

    return flank_dict

def _compute_flanks_methylation_proper_bed(
    flank_size: int, flank_dict: OrderedDict, infile: str, depth_limit: int = 10, motif: str = "CG"
):
    """Computes methylation of flanks
    
    Parameters
    ----------

    flank_size : int, number of nucleotides flanking CN to analyse (max 3)
    flank_dict : dict, disctionary of flanks to store statistics
    infile : str, input file with sequences and methylation data
    depth_limit : int, sets a treshold for sequencing depth, default = 10,
        a minimum number of sequencing depth to take cytosine into analysis
    
    Returns
    -------

    flank_dict : dict, dictionary of flanks and methylation statistics
    """
    seq_start = int(22 / 2 - len(motif) / 2 - flank_size)
    seq_end = int(22 / 2 + len(motif) / 2 + flank_size)
    
    with open(infile, "r") as fh:
        data = fh.readlines()
        for line in data:
            elements = line.split()
            column4 = elements[3].split(":")
            sequence = column4[0]
            data = column4[1].split(";")
            mC, total = data[0], data[1]
            
            # header, sequence = line.split()
            # header_splited = header.split(":")[0].split(";")
            # mC, total = header_splited[0], header_splited[1]
            depth = int(total)
            if depth >= depth_limit:
                flank = sequence.upper()[seq_start:seq_end]
                if flank in flank_dict.keys():
                    meth_level = int(mC) / depth  # methylation level
                    flank_dict[flank][0] += 1  # increament count
                    flank_dict[flank][
                        1
                    ] += meth_level  # add methylation level to compute average at the end

    # compute average methylation
    for key, value in flank_dict.items():
        if value[0] > 0:
            flank_dict[key][1] = value[1] / value[0]

    return flank_dict


def _compute_flanks_frequencies(
    flank_size: int, flank_dict: OrderedDict, infile: str, motif: str = "CG"
):
    """Computes methylation of flanks
    
    Parameters
    ----------

    flank_size : int, number of nucleotides flanking CN to analyse (max 3)
    flank_dict : dict, disctionary of flanks to store statistics
    infile : str, input file with sequences and methylation data
    
    Returns
    -------

    flank_dict : dict, dictionary of flanks containing number of found flanks
    """
    seq_start = int(22 / 2 - len(motif) / 2 - flank_size)
    seq_end = int(22 / 2 + len(motif) / 2 + flank_size)

    with open(infile, "r") as fh:
        data = fh.readlines()
        for line in data:
            _, sequence = line.split()
            flank = sequence.upper()[seq_start:seq_end]
            if flank in flank_dict.keys():
                flank_dict[flank][0] += 1  # increament count
            line = fh.readline()

    return flank_dict

def _save_data(data: OrderedDict[str, list], outfile: str):
    """Saves methylation of flanks into file
    
    Parameters
    ----------
    data : dict, dictionary, where key=flank, value=list[counts,methylation]
    outfile : str, file name to write data
    """
    with open(outfile, "a+") as sh:
        header_to_data = ";".join(["Site", "Occurence", "Av. mC\n"])
        sh.write(header_to_data)
        for key, values in data.items():
            to_write = ";".join([key, str(values[0]), str(values[1])])
            sh.write(to_write)
            sh.write("\n")
        sh.write("\n")

if __name__ == "__main__":
    main()
