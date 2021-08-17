"""
Train
=====
Defines functions which train models and write model artifacts to disk.
"""
from __future__ import print_function

import pickle

import pandas as pd
from sklearn.tree import DecisionTreeRegressor

def train(x, y):
    """
    Train a decision tree regressor using a floating point feature matrix and
    a regression target.

    Arguments:
        x (~np.ndarray): The user feature matrix. (n_samples, n_features)
        y (~np.ndarray): The regression target. (n_samples, 1)

    Returns:
        model (sklearn.tree.DecisionTreeRegressor): The trained decision tree.
    """
    model = DecisionTreeRegressor(min_samples_leaf=1)
    model.fit(x, y)
    return model


def main(ta):
    """
    Load features and labels, train the tree, and serialize model artifact.

    Note: This is the training entrypoint used by baklava!
    """
    # Read in the training data
    data = ta.input_as_dataframe(channel='training')
    print(data)
    # Extract features and labels
    x = data[['age', 'height']]
    y = data['weight']

    # Fit the model to the data
    model = train(x, y)
    ta.log_metric({'accuracy': 0.8})
    # Save model object using pickle format
    with open(ta.artifact_path(filename='model.pkl'), 'wb') as stream:
        pickle.dump(model, stream)

    ta.log_artifact(model)

    print('Success!')

