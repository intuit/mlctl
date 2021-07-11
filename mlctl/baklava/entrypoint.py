"""
Entrypoint
==========
Common operations for handling entrypoint parsing and error checking for both
training and prediction images.
"""


def get(entry, key, name=None):
    """
    Get the entrypoint tuple

    Args:
        entry (dict[str, list[str]): Mapping from types of entrypoints to
            lists of entrypoints for that type.
        key (str): The type of entrypoint to look
            for (i.e. baklava.train)
        name (str): The name of the entrypoint to choose from the list of
            entrypoints. This does not need to be set if only one entrypoint
            exists for the specified section.

    Returns:
        name (str): The name of the entrypoint
        package (str): The package path to access the entrypoint function
        func (str): The name of the function
    """
    assert entry is not None, RuntimeError(
        'To dockerize a distribution, you must define a {} entrypoint'
        .format(key)
    )
    assert key in entry, RuntimeError(
        'To dockerize a using the specified command, you must specify an '
        'entrypoint under the {} key'.format(key)
    )

    assert isinstance(entry[key], list), RuntimeError(
        'Expected a {} of entrypoints in the {} section. Got a {} instead'
        .format(list, key, type(entry[key]))
    )

    assert len(entry[key]) > 0, RuntimeError(
        'No entrypoints specified in the setup.py file. The section {} exists '
        'but there are no entrypoints in the list'.format(key)
    )

    if name is None:
        assert len(entry[key]) == 1, RuntimeError(
            'Multiple entrypoints found for {}. You must specify which one '
            'to use with the entrypoint flag (e.g. python setup.py docker '
            '--entrypoint=main)'.format(key)
        )
        return parse(entry[key][0])

    mapping = mapped(entry[key])

    assert name in mapping, RuntimeError(
        'User specified the {} entrypoint within the {} section but this was '
        'not found. Valid options are: {}'
        .format(name, key, ', '.join(mapping.keys()))
    )

    return mapping[name]


def parse(entrypoint):
    """
    Parse an entrypoint string

    Args:
        entrypoint (str): The entrypoint string to parse.

    Returns:
        name (str): The name of the entrypoint
        package (str): The package path to access the entrypoint function
        func (str): The name of the function
    """
    equals = entrypoint.count('=')
    colons = entrypoint.count('=')

    assert equals == 1 and colons == 1, RuntimeError(
        'Invalid entrypoint format: "{}" Expected: '
        '"alias = package.module:function"'
        .format(entrypoint)
    )

    name, path = map(str.strip, entrypoint.split('='))
    package, func = path.split(':')
    return name, package, func


def mapped(entrypoints):
    """
    Get the list of entrypoints from the setup script and convert it
    into a map from name to package path and function tuple

    Arguments:
         entrypoints (list[str]): The list of entrypoints defined in the
            setup.py script.

    Returns:
        map (dict[str, tuple[str, str, str]): Mapping from name of the entrypoint
            to the name, package path, and function tuple.
    """
    result = dict()
    for entrypoint in entrypoints:
        name, package, func = parse(entrypoint)
        result[name] = (name, package, func)
    return result
