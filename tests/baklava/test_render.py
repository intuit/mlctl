import os
import shutil
import tempfile
import contextlib

from baklava import render


@contextlib.contextmanager
def tempdir():
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


def test_example_template():

    name = 'test'
    value = '1'

    with tempdir() as path:

        source = os.path.join(os.path.dirname(__file__), 'template')

        render.copy(source, path, name=name, value=value)

        directory = os.path.join(path, name)
        assert os.path.isdir(directory)

        filename = os.path.join(directory, "{}.txt".format(name))
        assert os.path.exists(filename)

        with open(filename) as stream:
            data = stream.read()

        assert value == data


if __name__ == '__main__':
    test_example_template()
