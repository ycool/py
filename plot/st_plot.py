"""
display hd map
"""
import sys
import numpy
from proto import map_pb2
from proto import st_plot_pb2
from google.protobuf import text_format
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import random
import argparse

g_axis = None

def draw_text(text, x, y):
    """
    :param text
    :param x
    :param y
    """
    g_axis.text(x, y, text)


def plot_st_polygon(points, name):
    """
    :param polygon:
    :return:
    """
    if len(points) < 3:
        return
    px = [float(p.t) for p in points]
    py = [float(p.s) for p in points]
    px.append(px[0])
    py.append(py[0])
    g_axis.plot(px, py, 'b')
    draw_text(name, px[0], py[0])


def parse_proto_data(filename, proto_type):
    """
    :param filename
    """
    global g_axis
    f, g_axis = plt.subplots()
    f = open(args.file, 'r')
    st_plot_data = f.read()
    data_buf = proto_type()
    text_format.Merge(str(st_plot_data), data_buf)
    return data_buf


def plot_st_decision(st_decisions):
    """
    :param st_decisions
    """
    for st_decision in st_decisions:
        text = st_decision.object_id
        tag = ""
        if not st_decision.made_decision:
            tag = "NoDecision"
        elif st_decision.decision.HasField("stop"):
            tag = "Stop"
        elif st_decision.decision.HasField("ignore"):
            tag = "Ignore"
        elif st_decision.decision.HasField("yield"):
            tag = "Yield"
        elif st_decision.decision.HasField("overtake"):
            tag = "Overtake"
        elif st_decision.decision.HasField("follow"):
            tag = "Follow"
        plot_st_polygon(st_decision.polygon, st_decision.object_id + "#" + tag)


def plot_cell(cell, delta_s, delta_t):
    """
    :param cell
    :param delta_s
    :param delta_t
    """
    if cell.occupied:
        g_axis.plot(cell.origin.t, cell.origin.s, 'r.')
    if random.randint(0, 200)  % 200 == 0:
        draw_text(str(cell.cost), cell.origin.t, cell.origin.s)


def plot_st_matrix(st_matrix, st_constraint):
    """
    :param st_matrix
    :param st_constraint
    """
    for row in st_matrix.st_row:
        for cell in row.st_cell:
            plot_cell(cell, st_constraint.delta_s, st_constraint.delta_t)


def plot_st_path(st_path):
    """
    :param st_path
    """
    px = [p.t for p in st_path]
    py = [p.s for p in st_path]
    g_axis.plot(px, py, 'g.-')


def plot_st_speed_profile(st_speed):
    """
    :param st_path
    """
    px = [p.t for p in st_speed.max_speed.point]
    py = [p.s for p in st_speed.max_speed.point]
    g_axis.plot(px, py, 'c.-')
    px = [p.t for p in st_speed.min_speed.point]
    py = [p.s for p in st_speed.min_speed.point]
    g_axis.plot(px, py, 'c.-')

if __name__ == "__main__":
    VERSION_NUMBER = "0.0.1"
    parser = argparse.ArgumentParser(description="plot st graph" \
            , prog="st_plot.py")
    parser.add_argument("file", action="store", type=str, help="specify the proto buf to plot")
    parser.add_argument("-v", "--version", action="store_true" \
            , help="get the version information")
    args = parser.parse_args()

    st_plot = parse_proto_data(args.file, st_plot_pb2.StPlot)

    t_range = st_plot.st_constraint.delta_t * st_plot.st_matrix.t_num
    s_range = st_plot.st_constraint.delta_s * st_plot.st_matrix.s_num

    plot_st_decision(st_plot.st_decision)
    plot_st_matrix(st_plot.st_matrix, st_plot.st_constraint)
    plot_st_path(st_plot.st_path.point)
    plot_st_speed_profile(st_plot.st_speed)

    plt.xlim(-1, t_range)
    plt.ylim(-10, s_range)
    g_axis.set_xticks(numpy.arange(0, t_range, 1))
    g_axis.set_yticks(numpy.arange(0, s_range, 10))
    plt.grid()
    plt.show()
