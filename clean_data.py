"""Modulo principale per pulire i dati."""
import re
import argparse

import numpy as np
import pandas as pd


def delete_dots(line):
    """Delete multiple .. from a text line."""
    return re.sub(r"\.\.", r"", line)


def clean_file(infile_path, outfile_path):
    """Clean a file from spurious contents like `..`"""
    with open(infile_path, "r") as infile:
        result = [delete_dots(line) for line in infile.readlines()]

    with open(outfile_path, "w") as outfile:
        outfile.writelines(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The input file to clean")
    parser.add_argument("output_file", help="The output, cleaned file")
    args = parser.parse_args()

    print("Cleaning file {} and saving to {}".format(args.input_file,
                                                     args.output_file))
    clean_file(args.input_file, args.output_file)
    print("Finished!")
