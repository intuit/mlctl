import re

from baklava import environment


def test_get_environment_variables():
    mapping = environment.get_environment_variables()

    # Check that the keys are properly generated. We can't know for sure in each
    # environment what the values will be
    assert 'pip_index_url' in mapping
    assert 'pip_trusted_host' in mapping
    assert 'pip_extra_index_url' in mapping


def test_get_python_version():
    version = environment.get_python_version()
    assert re.match(r'\d\.\d', version) is not None
