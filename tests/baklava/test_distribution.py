from baklava import distribution, entrypoint

# ------------------------------------------------------------------------------
# Format Dockerlines
# ------------------------------------------------------------------------------

block = """
RUN hello
RUN world
"""

block_indent = """
               RUN hello
               RUN world
               """


def test_format_dockerlines_block():
    result = distribution.format_dockerlines(block)
    assert result == block


def test_format_dockerlines_block_indent():
    result = distribution.format_dockerlines(block_indent)
    assert result == block


def test_format_dockerlines_line():
    line = "RUN hello"
    result = distribution.format_dockerlines(line)
    assert result == line


def test_format_dockerlines_single_item_list():
    items = [
        "RUN hello",
    ]
    expected = "RUN hello"
    result = distribution.format_dockerlines(items)
    assert result == expected


def test_format_dockerlines_multi_item_list():
    items = [
        "RUN hello",
        "RUN world",
    ]
    expected = '\n'.join(items)
    result = distribution.format_dockerlines(items)
    assert result == expected


def test_format_dockerlines_none():
    dockerlines = None
    expected = ""
    result = distribution.format_dockerlines(dockerlines)
    assert result == expected


def test_format_dockerlines_empty_list():
    dockerlines = []
    expected = ""
    result = distribution.format_dockerlines(dockerlines)
    assert result == expected


def test_format_dockerlines_empty_string():
    dockerlines = ""
    expected = ""
    result = distribution.format_dockerlines(dockerlines)
    assert result == expected


# ------------------------------------------------------------------------------
# Format Dockerlines
# ------------------------------------------------------------------------------

def test_format_requirements_single():
    requirements = ["hello"]
    expected = 'RUN pip install --no-cache-dir hello'
    result = distribution.format_requirements(requirements)
    assert result == expected


def test_format_requirements_multiple():
    requirements = ["hello", "world==2"]
    expected = 'RUN pip install --no-cache-dir hello world==2'
    result = distribution.format_requirements(requirements)
    assert result == expected


def test_format_requirements_empty_list():
    requirements = []
    expected = ''
    result = distribution.format_requirements(requirements)
    assert result == expected


def test_format_requirements_empty_none():
    requirements = None
    expected = ''
    result = distribution.format_requirements(requirements)
    assert result == expected


# ------------------------------------------------------------------------------
# Format Entrypoint
# ------------------------------------------------------------------------------

def test_format_entrypoints_success():
    inputs = 'alias = package.module:function'
    alias = 'sample'
    expected = 'from package.module import function as sample'

    parsed = entrypoint.parse(inputs)
    result = distribution.format_entrypoints(parsed, alias)
    assert result == expected


def test_format_entrypoints_no_entrypoint():
    parsed = (None, None, None)
    alias = 'sample'
    expected = 'sample = None'

    result = distribution.format_entrypoints(parsed, alias)
    assert result == expected


# ------------------------------------------------------------------------------
# Format Entrypoint
# ------------------------------------------------------------------------------

def test_build_parameters_success():
    result = distribution.build_parameters(
        archive="example",
        entrypoint=(None, None, None),
        requirements=[],
        python_version="5",
        dockerlines=None
    )
    assert "python_version" in result
    assert "distribution" in result
    assert "requirements" in result
    assert "dockerlines" in result
    assert "entrypoint" in result


if __name__ == '__main__':
    test_format_dockerlines_block()
    test_format_dockerlines_block_indent()
    test_format_dockerlines_line()
    test_format_dockerlines_single_item_list()
    test_format_dockerlines_multi_item_list()
    test_format_dockerlines_none()
    test_format_dockerlines_empty_list()
    test_format_dockerlines_empty_string()
    test_format_requirements_single()
    test_format_requirements_multiple()
    test_format_requirements_empty_list()
    test_format_requirements_empty_none()
    test_format_entrypoints_no_entrypoint()
    test_build_parameters_success()