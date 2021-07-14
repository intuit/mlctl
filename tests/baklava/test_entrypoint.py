import pytest
from baklava import entrypoint


entries = {
    'baklava.train': [
        'alias1 = package1.module1:function1',
        'alias2 = package2.module2:function2',
        'alias3 = package3.module3:function3',
    ],
    'baklava.predict': [
        'alias = package.module:function',
    ],
    'console_scripts': [
        'alias = package.module:function',
    ],
}


train = 'baklava.train'
predict = 'baklava.predict'


@pytest.mark.xfail(raises=AssertionError)
def test_entrypoint_get_ambiguous():
    """Error when ambiguous reference"""
    entrypoint.get(entries, train)


@pytest.mark.xfail(raises=AssertionError)
def test_entrypoint_get_empty():
    """Error when empty entries are provided"""
    entrypoint.get({}, train)


@pytest.mark.xfail(raises=AssertionError)
def test_entrypoint_get_none():
    """Error when no entry provided"""
    entrypoint.get(None, train)


@pytest.mark.xfail(raises=AssertionError)
def test_entrypoint_get_type_error():
    """Error when no entry provided"""
    entrypoint.get({'baklava.train': 'error'}, train)


@pytest.mark.xfail(raises=AssertionError)
def test_entrypoint_get_empty_list():
    """Error when no entry provided"""
    entrypoint.get({'baklava.train': []}, train)


def test_entrypoint_get_single():
    """Single unambiguous entrypoint"""
    name, package, func = entrypoint.get(entries, predict)
    assert name == 'alias'
    assert package == 'package.module'
    assert func == 'function'


def test_entrypoint_get_multiple():
    """Multiple entrypoint with specifier"""
    name, package, func = entrypoint.get(entries, train, 'alias2')
    assert name == 'alias2'
    assert package == 'package2.module2'
    assert func == 'function2'


def test_parse():
    string = ' alias = package.module:function '
    name, package, func = entrypoint.parse(string)
    assert name == 'alias'
    assert package == 'package.module'
    assert func == 'function'


def test_parse_no_space():
    string = 'alias=package.module:function'
    name, package, func = entrypoint.parse(string)
    assert name == 'alias'
    assert package == 'package.module'
    assert func == 'function'


@pytest.mark.xfail(raises=AssertionError)
def test_parse_comma_error():
    string = (
        'alias = package.module:function'
        'alias = package.module:function'
    )
    entrypoint.parse(string)


if __name__ == '__main__':
    pytest.main([__file__])
