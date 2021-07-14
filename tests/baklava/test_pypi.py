import os
import uuid
import contextlib
import tempfile

from baklava import pypi


@contextlib.contextmanager
def pushenv():
    original = os.environ.copy()
    yield
    os.environ = original


def test_load_env():

    with pushenv():
        # Set environment variables (Top Precedence)
        index = str(uuid.uuid4())
        extra = str(uuid.uuid4())
        os.environ['PIP_INDEX_URL'] = index
        os.environ['PIP_EXTRA_INDEX_URL'] = extra

        # API Call
        config = pypi.load()

        # Assertions
        assert config['index-url'] == index
        assert config['extra-index-url'] == extra


def test_invalid_config_path():
    with pushenv():
        filename = str(uuid.uuid4())
        os.environ["PIP_CONFIG_FILE"] = filename
        config = pypi.load()
        assert config['config-file'] == filename


def test_invalid_config_content():

    temp = tempfile.NamedTemporaryFile()

    with open(temp.name, 'wb') as handle:
        handle.write(b"\001")

    with pushenv():
        os.environ["PIP_CONFIG_FILE"] = temp.name
        config = pypi.load()
        assert config['config-file'] == temp.name


if __name__ == '__main__':
    test_load_env()
    test_invalid_config_path()
    test_invalid_config_content()
