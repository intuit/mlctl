#####################################################################
## Version
#####################################################################

try:
    from mlctl.__version import __version__  # type: ignore
except ImportError:  # pragma: no cover
    __version__ = "dev"