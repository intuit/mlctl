import click
import os
from click.testing import CliRunner

from unittest import mock
import unittest

from mlctl.clis.init_cli import init
from cookiecutter.utils import rmtree


class TestInitCli(unittest.TestCase):

    def test_init(self):
        # run command in home dir
        os.chdir(os.path.expanduser('~'))
        runner = CliRunner()
        response = runner.invoke(init, ['-v'], input='Sample Project')

        # prints this message in verbose mode
        self.assertIn(
            "DEBUG - Creating ML Model project using template from", response.output)

        # check the details of the initialized model
        project_path = os.path.join(
            os.path.expanduser('~'), "sample_project")
        project_slug = os.path.split(project_path)[-1]
        project_dir = os.path.join(project_path, project_slug)

        # checks content of the sample model code
        self.assertTrue(os.path.exists(project_path))
        self.assertTrue(os.path.exists(
            os.path.join(project_path, "model/predict.py")))
        self.assertTrue(os.path.exists(
            os.path.join(project_path, "model/train.py")))
        self.assertTrue(os.path.exists(
            os.path.join(project_path, "model/__init__.py")))
        self.assertTrue(os.path.exists(
            os.path.join(project_path, "tests/__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(
            project_path, "tests/test_sample_project.py")))
        self.assertTrue(os.path.exists(os.path.join(
            project_path, ".github/ISSUE_TEMPLATE.md")))
        self.assertTrue(os.path.exists(
            os.path.join(project_path, ".gitignore")))
        self.assertTrue(os.path.exists(
            os.path.join(project_path, "README.md")))
        self.assertTrue(os.path.exists(
            os.path.join(project_path, "setup.cfg")))
        self.assertTrue(os.path.exists(os.path.join(project_path, "setup.py")))
        self.assertTrue(os.path.exists(os.path.join(project_path, "tox.ini")))

        # removes model code from local directory
        rmtree(str(project_path))
