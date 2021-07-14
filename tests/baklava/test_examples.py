from __future__ import print_function

import os
import tempfile
import re
import subprocess

import pytest
import docker
from docker.utils.json_stream import json_stream


import baklava


# ------------------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------------------

def example(name='1-simple-functions'):
    """
    Get the path to the example directory

    Args:
        name (str): The name of the example to get the path for

    Returns:
        path (str): The example directory path
    """
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'examples',
        name,
    )


def tmp():
    """
    Get the path to a new temporary file

    Returns:
        path (str): The temporary file path
    """

    return tempfile.NamedTemporaryFile(delete=False).name


# ------------------------------------------------------------------------------
# Basic Build
# ------------------------------------------------------------------------------

examples = [
    '1-simple-functions',
    '2-sagemaker-paths',
    '3-sklearn-tree',
    '4-tensorflow-mnist',
    '6-internal-dependencies',
    '7-custom-docker-lines',
    '9-non-python-files',
]


@pytest.mark.slow
@pytest.mark.parametrize("name", examples)
def test_train_build(name):
    """Check that basic train image builds successfully"""
    code = baklava.train(example(name), [])
    assert code == 0


@pytest.mark.slow
@pytest.mark.parametrize("name", examples)
def test_predict_build(name):
    """Check that basic predict image builds successfully"""
    code = baklava.predict(example(name), [])
    assert code == 0


# ------------------------------------------------------------------------------
# 1-simple-functions
# ------------------------------------------------------------------------------

@pytest.mark.slow
def test_1_simple_functions_train_idfile():
    """Check that the id file can be extracted from build procedure"""

    idfile = tmp()
    code = baklava.train(example(), ['--idfile={}'.format(idfile)])

    assert code == 0

    with open(idfile) as stream:
        content = stream.read()

    # The content of the idfile will look like the docker sha checksum:
    # sha256:e422a43d58ceccc77283145bdb42312461cb67fd90e66bc5bc2fe59af51bdf8c
    assert re.match("sha256\:[0-9a-f]{64}", content) is not None


@pytest.mark.slow
def test_1_simple_functions_train_execute():
    """Check that the docker image executes successfully"""

    process = baklava.api.run(
        path=example(),
        cmd='train',
        args=['-t', 'test-image']
    )
    assert process.returncode == 0, 'Failed to build image'

    client = docker.from_env()
    response = client.containers.run('test-image')

    stdout = response.decode('utf8')
    assert re.search("Hello World", stdout) is not None


# ------------------------------------------------------------------------------
# 5-multiple-images
# ------------------------------------------------------------------------------

@pytest.mark.slow
@pytest.mark.parametrize("entrypoint, expected", [
    ('first', 'Train 1!'),
    ('second', 'Train 1!'),
    ('third', 'Train 2!'),
])
def test_5_multiple_images_train_execute(entrypoint, expected):
    process = baklava.api.run(
        path=example('5-multiple-images'),
        cmd='train',
        args=['--entrypoint', entrypoint, '-t', 'test-image'],
    )
    assert process.returncode == 0, 'Failed to build image'

    client = docker.from_env()
    response = client.containers.run('test-image')

    stdout = response.decode('utf8')
    assert re.search(expected, stdout) is not None


# ------------------------------------------------------------------------------
# 7-custom-docker-lines
# ------------------------------------------------------------------------------

@pytest.mark.slow
def test_7_build_and_check():
    # Get the path to the artifacts
    dist = os.path.join(example('7-custom-docker-lines'), 'dist')

    # Build the image using low level API to get output directly
    client = docker.from_env()
    response = client.api.build(
        path=dist,
        quiet=False,
        nocache=True,
    )

    # Check to see that custom run command and its output exists
    found_command = False
    found_output = False
    for chunk in json_stream(response):
        if 'stream' in chunk:
            formatted = chunk['stream'].rstrip()

            # Check if we ever see the run command
            if re.search('RUN echo hello world$', formatted):
                found_command = True

            # If we saw the run command, check for output
            if found_command and re.search('^hello world$', formatted):
                found_output = True

    assert found_command
    assert found_output


@pytest.mark.slow
def test_7_custom_docker_lines_train():
    """Check that setup.py dockerlines works as expected for training"""

    # Build the distribution without building the image
    code = baklava.train(example('7-custom-docker-lines'), ['--nobuild'])
    assert code == 0

    test_7_build_and_check()


@pytest.mark.slow
def test_7_custom_docker_lines_predict():
    """Check that setup.py dockerlines works as expected for prediction"""

    # Build the distribution without building the image
    code = baklava.predict(example('7-custom-docker-lines'), ['--nobuild'])
    assert code == 0

    test_7_build_and_check()


# ------------------------------------------------------------------------------
# 8-predict-initializer
# ------------------------------------------------------------------------------

@pytest.mark.slow
def test_8_predict_initializer():
    """Test that the predict initializer example builds correctly"""

    code = baklava.predict(example('8-predict-initializer'), [])
    assert code == 0


# ------------------------------------------------------------------------------
# 9-non-python-files
# ------------------------------------------------------------------------------

@pytest.mark.slow
def test_9_non_python_files():
    """Check that setup.py python_version works as expected"""

    name = '9-non-python-files'
    code = baklava.train(example(name), ['--nobuild'])
    assert code == 0

    dist = os.path.join(example(name), 'dist')

    # Build the image using low level API to get output directly
    client = docker.from_env()
    response = client.api.build(
        path=dist,
        quiet=False,
        nocache=True,
    )

    # Check to see that custom run command and its output exists
    for chunk in json_stream(response):
        if 'stream' in chunk:
            formatted = chunk['stream'].rstrip()
            print(formatted)
            if re.search('FROM python:2\.7\.15-slim$', formatted):
                return

    # If we made it here, we did not find the correct python version
    assert False


# ------------------------------------------------------------------------------
# Train flags (Sanity Tests)
# ------------------------------------------------------------------------------

@pytest.mark.slow
def test_flag_train_nobuild():
    """Test that training image nobuild flag succeeds"""

    name = '1-simple-functions'
    code = baklava.train(example(name), args=['--nobuild'])
    assert code == 0


@pytest.mark.slow
def test_flag_train_idfile():
    """Test that training image idfile argument succeeds"""

    name = '1-simple-functions'
    code = baklava.train(example(name), args=['--idfile=id.txt'])
    assert code == 0


# ------------------------------------------------------------------------------
# Predict flags (Sanity Tests)
# ------------------------------------------------------------------------------

@pytest.mark.slow
def test_flag_predict_nobuild():
    """Test that predict image nobuild flag succeeds"""

    name = '1-simple-functions'
    code = baklava.predict(example(name), args=['--nobuild'])
    assert code == 0


@pytest.mark.slow
def test_flag_predict_idfile():
    """Test that predict image idfile argument succeeds"""

    name = '1-simple-functions'
    code = baklava.predict(example(name), args=['--idfile=id.txt'])
    assert code == 0


@pytest.mark.slow
def test_flag_predict_workers():
    """Test that predict image workers argument succeeds"""

    name = '1-simple-functions'
    code = baklava.predict(example(name), args=['--workers=10'])
    assert code == 0


if __name__ == '__main__':
    pytest.main([__file__, '--slow'])
