"""
Distribution
============
Functions for building distribution artifacts prior to building docker images
"""
import pkg_resources
import os
import textwrap

from baklava import environment, render


def format_dockerlines(dockerlines):
    """
    Ensures docker lines are correctly formatted.

    Users may input either a string or a list of strings in the setup.py. This
    method ensures that the format is correct regardless of input type.

    Arguments:
        dockerlines (Union[str, list[str]]): The dockerlines provided by the
            python distribution setup file.

    Returns:
        dockerlines (str): The block of dockerlines to insert into the template
    """
    if dockerlines in (None, "", []):
        return ""

    assert isinstance(dockerlines, (list, str)), TypeError(
        'Docker lines must be a list or string. Got {}'
        .format(type(dockerlines))
    )

    if isinstance(dockerlines, str):
        return textwrap.dedent(dockerlines)

    return '\n'.join(dockerlines)


def format_requirements(requirements):
    if requirements in (None, "", []):
        return ""

    return "RUN pip install --no-cache-dir {}".format(' '.join(requirements))


def format_entrypoints(entrypoint, alias):
    name, package, func = entrypoint
    if name is None:
        return "{alias} = None".format(alias=alias)
    return 'from {package} import {func} as {alias}'.format(package=package, func=func, alias=alias)


def build_parameters(archive, entrypoint, requirements, python_version, dockerlines):

    # Load PyPI environment
    env = environment.get_environment_variables()

    # Set python version to environment python version
    if python_version is None:
        python_version = environment.get_python_version()

    # Make sure dockerlines are properly formatted
    dockerlines = format_dockerlines(dockerlines)
    requirements = format_requirements(requirements)
    entrypoint = format_entrypoints(entrypoint, 'entrypoint')

    # Write dockerfile
    return dict(
        python_version=python_version,
        distribution=archive,
        requirements=requirements,
        dockerlines=dockerlines,
        entrypoint=entrypoint,
        **env
    )


def train(path, archive, entrypoint, requirements, python_version, dockerlines):
    """
    Create docker-specific training image artifacts

    Args:
        path (str): The directory to the distribution path to save artifacts to
        archive (str): The path to the source distribution
        entrypoint (str): The package entrypoint
        requirements (list[str]): The list of package requirements
        python_version (str): The specific version of python to use
        dockerlines (Union[str, list[str]]): Dockerlines provided by setup file

    Returns:
        artifacts (list[str]): The collection of artifacts used to create a
            training image.
    """
    # Common parameters
    parameters = build_parameters(archive, entrypoint, requirements, python_version, dockerlines)

    # Render the result
    src = pkg_resources.resource_filename('baklava.resources', 'train')
    files = render.copy(src, path, **parameters)

    # Return all distribution files
    files.append(os.path.join(path, archive))
    return files


def predict(path, archive, entrypoint, requirements, initializer, python_version, dockerlines, workers=8):
    """
    Create docker-specific prediction image artifacts

    Args:
        path (str): The directory to the distribution path to save artifacts to
        archive (str): The path to the source distribution
        entrypoint (str): The package entrypoint
        requirements (list[str]): The list of package requirements
        initializer (str): The initization entrypoint to the package
        python_version (str): The specific version of python to use
        dockerlines (Union[str, list[str]]): Dockerlines provided by setup file
        workers (int): The number of worker processes to spawn in the image

    Returns:
        artifacts (list[str]): The collection of artifacts used to create a
            prediction image.
    """

    # Common parameters
    parameters = build_parameters(archive, entrypoint, requirements, python_version, dockerlines)

    # Update parameters with options
    initializer = format_entrypoints(initializer, 'initializer')

    parameters.update(
        initializer=initializer,
        workers=workers,
    )

    # Render the result
    src = pkg_resources.resource_filename('baklava.resources', 'predict')
    files = render.copy(src, path, **parameters)

    # Return all distribution files
    files.append(os.path.join(path, archive))
    return files
