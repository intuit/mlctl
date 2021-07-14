"""
API
===
Python API for dockerizing python packages.
"""
import subprocess
import os
import sys


def run(path, cmd, args, stdout=None, stderr=None):
    """
    Runs a python packaging command on a specified directory

    .. note::
        This uses a subprocess call rather than importing the setup file
        directly because there is no guarantee how the setup file could be
        structured.

    Arguments:
        path (str): The path where the package directory and :literal:`setup.py`
            are located
        cmd (str): The specific setuptools command to run
        args (list[str]): The arguments to pass to the predict command. By
            default the system arguments are used.
        stdout (int): The subprocess option to choose how to
            capture the stdout stream (Should only be used for testing)
        stderr (int): The subprocess option to choose how to
            capture the stderr stream (Should only be used for testing)

    Returns:
        process (subprocess.Popen): The process that was run
    """
    path = os.path.abspath(path)

    args = [
        'python',
        '{path}/setup.py'.format(path=path),
        cmd,
    ] + args

    process = subprocess.Popen(args, cwd=path, stdout=stdout, stderr=stderr)
    process.wait()
    return process


def train(path=os.getcwd(), args=None):
    """
    Build a training container for a python package.

    Arguments:
        path (str): The path where the package directory and :literal:`setup.py`
            are located.
        args (list[str]): The arguments to pass to the train command. By
            default the system arguments are used.

    Returns:
        code (int): The process return code
    """
    return run(path, 'train', args).returncode


def predict(path=os.getcwd(), args=None):
    """
    Build a prediction container for a python package.

    Arguments:
        path (str): The path where the package directory and :literal:`setup.py`
            are located.
        args (list[str]): The arguments to pass to the predict command. By
            default the system arguments are used.

    Returns:
        code (int): The process return code
    """
    return run(path, 'predict', args).returncode
