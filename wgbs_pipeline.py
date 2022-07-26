#!/usr/bin/env python
################################################################################
# This script is written by Pavel Bashtrykov
# pavel.bashtrykov@ibtb.uni-stuttgart.de
# pavel.bashtrykov@gmail.com
################################################################################

import os
import json


def main():
    """
    Pipeline to analyse whole-genome bisulfite sequencing data.
    List of SRA ids and commands are written in the config.json file, which has to be in the same working directory.
    """
    # Load configuration
    rep_path = os.path.dirname(__file__)

    config_file = "config.json"
    conf_file_path = os.path.join(rep_path, config_file)
    conf = json.load(open(file=conf_file_path))

    # Get SRA ids
    ids = conf["sra_ids"]

    # Commands
    commands = conf["commands"]

    for f in ids:
        for c in commands:
            command = c.format(tag=f)
            print(f"Starting command: {command}")
            output = os.popen(command)
            for line in output:
                print(line.rstrip())
            print(f"Done with command: {command}")


if __name__ == "__main__":
    main()
