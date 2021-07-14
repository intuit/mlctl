"""
Render
======
Utilities for rendering folder templates using the core library string.Template
class.

Note: This module functions similar to the cookiecutter package except that it
does not have any external dependencies.
"""
import os
import string


def validate_directory(directory):
    """
    Raise an error if the directory does not exist or is not a directory.

    Args:
        directory (str): The path to the directory to check.
    """
    if not os.path.exists(directory):
        raise ValueError("Directory '{}' does not exist".format(directory))
    if not os.path.isdir(directory):
        raise ValueError("File '{}' is not a directory".format(directory))


def files(root):
    """
    Recursively get filename and directory paths from a root directory.

    Args:
        root (str): The root directory to get files from.

    Returns:
        filenames (list[str]): The collection of filenames and directories
            under the root directory.
    """
    filenames = list()
    for root, dirs, files in os.walk(root):
        for directory in dirs:
            if "__pycache__" in directory:
                continue
            filenames.append(os.path.join(root, directory))
        for name in files:
            if name.endswith(".pyc"):
                continue
            filenames.append(os.path.join(root, name))
    return filenames


def copy(source, destination, **replacements):
    """
    Recursively copy the contents of the source directory to the destination
    directory and replaces all template strings in both the file names and
    file contents.

    See: https://docs.python.org/3/library/string.html#template-strings

    Args:
        source (str): The path to the template root directory to read from.
        destination (str): The path to the directory to write to.

    Kwargs:
        replacements: A mapping from $-prefixed token to substitution.

    Returns:
        files (list[str]): The filenames in the destination folder.
    """
    # Validate that the source/destination directories exist
    validate_directory(source)
    validate_directory(destination)

    # Recursively get source files from template root
    sources = files(source)

    # Build destination paths from source paths
    destinations = list()
    for src in sources:

        # Strip off root
        size = len(source)
        relative = src[size:].lstrip(os.path.sep)

        # Substitute relative path filename
        result = string.Template(relative).safe_substitute(**replacements)
        destinations.append(os.path.join(destination, result))

    # Now loop through source files and write rendered files
    for src, dst in zip(sources, destinations):

        # Create the directory if source was a directory
        if os.path.isdir(src):
            os.makedirs(dst)
            continue

        # Write rendered files
        with open(src, "r") as template:
            with open(dst, "w") as rendered:
                content = template.read()
                result = string.Template(content).safe_substitute(**replacements)
                rendered.write(result)

    return destinations
