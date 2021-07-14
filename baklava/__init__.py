try:
    from mlctl.__version import __version__
except ImportError:  # pragma: no cover
    __version__ = 'dev'

from baklava.api import (
    train,
    predict,
)
