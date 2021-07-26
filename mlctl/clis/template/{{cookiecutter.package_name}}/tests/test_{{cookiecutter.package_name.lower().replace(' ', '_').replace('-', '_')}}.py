#!/usr/bin/env python

"""Tests for `{{ cookiecutter.package_name.lower().replace(' ', '_').replace('-', '_')  }}` package."""

import unittest

from {{ cookiecutter.package_name.lower().replace(' ', '_').replace('-', '_') }} import {{ cookiecutter.package_name.lower().replace(' ', '_').replace('-', '_') }}


class Test{{cookiecutter.package_name.lower().replace(' ', '_').replace('-', '_') | title}}(unittest.TestCase):
    """Tests for `{{ cookiecutter.package_name.lower().replace(' ', '_').replace('-', '_')  }}` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_train(self):
        """Test something."""
