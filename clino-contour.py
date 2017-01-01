#!/usr/bin/python
"""
================================================================================
INCLINOMETER PLOTTING
================================================================================
Plot data from a borehole inclinometer as a contour graph. Data is provided as
CSV files in the same directory as the script. Plots are also output to the same
directory as PNG files.
"""

import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
from csv import reader
from os import listdir, chdir
from os.path import isfile, join, dirname, abspath
from argparse import ArgumentParser


# ============================================================================ #
# ARGUMENTS
# ============================================================================ #
parser = ArgumentParser()
parser.add_argument("-i", "--input", help="TXT file with input values",
                    type=str)
args = parser.parse_args()


# ============================================================================ #
# FUNCTIONS
# ============================================================================ #
def is_csv(path):
    if isfile(path) and ".csv" in path:
        return True
    else:
        return False


def get_csv_filenames(path):
    return [file for file in listdir(path) if is_csv(join(path, file))]


def read_csv_file(path):
    with open(path) as csv_file:
        return [row for row in reader(csv_file, delimiter=",")]


def x_axis(headers):
    str_dates = [date.split(" ")[0] for date in headers[1:]]
    date_objs = [datetime.strptime(date, "%d/%m/%Y") for date in str_dates]
    date_objs.sort()
    return np.array(date_objs, dtype=object)


def y_axis(data):
    return [float(row[0]) for row in data[1:]]


def z_data(data):
    return np.array([row[1:] for row in data[1:]], dtype=np.float64)


def generate_plot(x, y, z):
    fig = plt.figure(figsize=(6, 4), dpi=300)
    colour_plot = plt.contourf(x, y, z, 10)
    key = plt.colorbar(colour_plot)
    key.ax.set_ylabel("Inclination")
    plt.title("Inclinometer Contour Plot")
    fig.autofmt_xdate()
    plt.tick_params(axis="x", labelsize=8)
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
    plt.ylabel("Depth (m)")
    plt.gca().invert_yaxis()
    fig.set_tight_layout(True)
    return plt


def plot(file):
    data = read_csv_file(file)
    contour = generate_plot(
        x_axis(data[0]),
        y_axis(data),
        z_data(data)
    )
    contour.savefig(join(".", "{0}.png".format(file.rstrip(".csv"))), dpi=300)


# ============================================================================ #
# MAIN BLOCK
# ============================================================================ #
if __name__ == "__main__":
    if args.input:
        plot(args.input)
    else:
        script_path = dirname(abspath(__file__))
        chdir(script_path)
        [plot(file) for file in get_csv_filenames(".")]
