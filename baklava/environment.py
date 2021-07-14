"""
Environment
===========
Functions dealing with specific environment configurations.
"""
import sys

from baklava import pypi


def get_environment_variables():
    """
    Use local pip installation to find environment variables that need to be
    set. This works both if using a `pip.conf` file or if using fixed
    environment variables.

    Returns:
        variables (dict[str, str]): The environment variables to set.
    """

    def fmt(x):
        return x.replace('\n', ' ').strip()

    options = pypi.load()

    return {
        'pip_index_url': fmt(options.get('index-url', "")),
        'pip_trusted_host': fmt(options.get('trusted-hosts', "")),
        'pip_extra_index_url': fmt(options.get('extra-index-url', "")),
    }


def get_python_version():
    """
    Get the python version string for the current version of python that is
    running.

    Returns:
        version (str): The major.minor version string
    """
    info = sys.version_info

    return '{major}.{minor}'.format(
        major=info.major,
        minor=info.minor,
    )
