"""
Module to get the transitions from file
"""
import csv
import logging
import os
import numpy as np
import pandas as pd

from definitions import ROOT_DIR


def get_transitions(person: str):
    """
    Formats the transition from a CSV file for every person given.

    :param person: person object
    :return: array with integer transitions
    """

    direc = os.path.join(ROOT_DIR, 'messenger', 'transition_matrices', f'transition_matrix_{person}.csv')
    df = pd.read_csv(direc, header=0, index_col=0)
    array = df.to_numpy()
    try:
        column_sums = np.sum(array, axis=0)
        assert np.allclose(column_sums, 1.0)
    except AssertionError:
        logging.critical(f"The Transition probabilities of {person} do not sum up to 1")

    return array
