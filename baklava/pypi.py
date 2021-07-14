"""
PyPI
====
Get PyPI indices in a way that is compatible with pip. This uses the same
locations and search precedence that pip uses.
"""
import os
from six.moves import configparser
import sys

import os.path
import appdirs
import warnings
import collections


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

config_basename = 'pip.conf'


class kinds:
    USER    = "user"     # User Specific
    GLOBAL  = "global"   # System Wide
    VENV    = "venv"     # Virtual Environment Specific
    ENV     = "env"      # from PIP_CONFIG_FILE
    ENV_VAR = "env-var"  # from Environment Variables


# ------------------------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------------------------

def running_under_virtualenv():
    """
    Return True if we're running inside a virtualenv, False otherwise.

    """
    if hasattr(sys, 'real_prefix'):
        return True
    elif sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return True
    return False


def get_legacy_file():
    if os.name == 'nt':
        return os.path.join(os.path.expanduser('~'), 'pip', 'pip.ini')
    return os.path.join(os.path.expanduser('~'), '.pip', 'pip.conf')


def get_site_config_file():
    return os.path.join(appdirs.site_config_dir('pip'), config_basename)


def get_venv_config_file():
    return os.path.join(sys.prefix, config_basename)


def get_new_config_file():
    return os.path.join(appdirs.user_config_dir("pip"), config_basename)


def normalize_name(name):
    # type: (str) -> str
    """Make a name consistent regardless of source (environment or file)
    """
    name = name.strip()
    name = name.lower().replace('_', '-')
    if name.startswith('--'):
        name = name[2:]  # only prefer long opts
    return name


def normalized_keys(section, items):
    # type: (str, Iterable[Tuple[str, Any]]) -> Dict[str, Any]
    """Normalizes items to construct a dictionary with normalized keys.

    This routine is where the names become keys and are made the same
    regardless of source - configuration files or environment.
    """
    normalized = {}
    for name, val in items:
        key = normalize_name(name)
        normalized[key] = val.strip()
    return normalized


def get_environ_vars():
    # type: () -> Iterable[Tuple[str, str]]
    """Returns a generator with all environmental vars with prefix PIP_"""
    for key, val in os.environ.items():
        should_be_yielded = (
                key.startswith("PIP_") and
                key[4:].lower() not in ["version", "help"]
        )
        if should_be_yielded:
            yield key[4:].lower(), val


# ------------------------------------------------------------------------------
# Configuration Loading
# ------------------------------------------------------------------------------

def iter_config_files():
    # type: () -> Iterable[Tuple[Kind, List[str]]]
    """Yields variant and configuration files associated with it.

    This should be treated like items of a dictionary.
    """
    legacy_config_file = get_legacy_file()
    venv_config_file = get_venv_config_file()
    site_config_files = get_site_config_file()
    new_config_file = get_new_config_file()

    # environment variables have the lowest priority
    config_file = os.environ.get('PIP_CONFIG_FILE', None)
    if config_file is not None:
        yield kinds.ENV, [config_file]
    else:
        yield kinds.ENV, []

    # at the base we have any global configuration
    yield kinds.GLOBAL, [site_config_files]

    # The legacy config file is overridden by the new config file
    if not (config_file and os.path.exists(config_file)):
        yield kinds.USER, [legacy_config_file, new_config_file]

    # finally virtualenv configuration first trumping others
    if running_under_virtualenv():
        yield kinds.VENV, [venv_config_file]


def load():
    config_files = dict(iter_config_files())

    override_order = [kinds.GLOBAL, kinds.USER, kinds.VENV, kinds.ENV, kinds.ENV_VAR]

    config = collections.defaultdict(lambda: dict())
    for variant, files in config_files.items():
        for fname in files:

            parser = configparser.RawConfigParser()

            # Read in file
            if os.path.exists(fname):
                try:
                    parser.read(fname)
                except:
                    warnings.warn('Unable to parse config file {}'.format(fname))
                    continue

            for section in parser.sections():
                items = parser.items(section)
                config[variant].update(normalized_keys(section, items))

    config[kinds.ENV_VAR].update(
        normalized_keys(":env:", get_environ_vars())
    )

    retval = {}
    for variant in override_order:
        retval.update(config[variant])
    return retval
