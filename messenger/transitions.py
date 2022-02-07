"""
Module to get the transitions from file
"""
import csv
import os
import numpy as np

from definitions import ROOT_DIR


def get_transitions(person: str):
    """
    Formats the transition from a CSV file for every person given.

    :param person: person object
    :return: array with integer transitions
    """
    important_lines1 = []
    important_lines2 = []
    important_lines3 = []
    important_lines4 = []
    important_lines5 = []
    important_lines6 = []
    important_lines7 = []
    important_lines8 = []
    important_lines9 = []
    important_lines10 = []

    direc = os.path.join(ROOT_DIR, 'messenger', 'whatsapp', 'modular_fsm_test', f'transition_matrix_{person}.csv')
    with open(direc) as fd:
        reader = csv.reader(fd)
        for i, j in enumerate(reader):
            if i == 2:
                important_lines1 = j[2:]
            elif i == 3:
                important_lines2 = j[2:]
            elif i == 4:
                important_lines3 = j[2:]
            elif i == 5:
                important_lines4 = j[2:]
            elif i == 6:
                important_lines5 = j[2:]
            elif i == 7:
                important_lines6 = j[2:]
            elif i == 8:
                important_lines7 = j[2:]
            elif i == 9:
                important_lines8 = j[2:]
            elif i == 10:
                important_lines9 = j[2:]
            elif i == 11:
                important_lines10 = j[2:]

    array = np.vstack([important_lines1,
                       important_lines2,
                       important_lines3,
                       important_lines4,
                       important_lines5,
                       important_lines6,
                       important_lines7,
                       important_lines8,
                       important_lines9,
                       important_lines10])

    array = array.astype(np.float)

    return array
