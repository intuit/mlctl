from baklava import images


def test_regular_version():
    result = images.tag([], 'example', '0.0.1')
    assert result.startswith('example:0.0.1')


def test_setuptools_scm_version():
    result = images.tag([], 'example', '0.0.26.dev6+g6099e47.d20200428')
    assert result.startswith('example:0.0.26.dev6.g6099e47.d20200428')

