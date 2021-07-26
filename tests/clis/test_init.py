import click
import os
from click.testing import CliRunner

from unittest import mock
import unittest

from mlctl.clis.init_cli import init
from cookiecutter.utils import rmtree
import filecmp


class TestInitCli(unittest.TestCase):

    def test_init(self):
        # run command in home dir
        project_path = os.path.join(os.path.expanduser('~'), 'test_mlctl_init')
        if os.path.isdir(project_path):
            rmtree(str(project_path))
        os.makedirs(project_path)
        os.chdir(project_path)
        runner = CliRunner()
        response = runner.invoke(init, ['-v'], input='Sample Project')

        # prints this message in verbose mode
        self.assertIn(
            "DEBUG - Creating ML Model project using template from", response.output)

        self.assertTrue(filecmp.cmp(os.path.join(project_path, "model/predict.py"),
                                    os.path.join(os.path.dirname(__file__), "mlctl_init/model/predict.py")))

        self.assertTrue(filecmp.cmp(os.path.join(project_path, "model/train.py"),
                                    os.path.join(os.path.dirname(__file__), "mlctl_init/model/train.py")))

        self.assertTrue(filecmp.cmp(os.path.join(project_path, "model/__init__.py"),
                                    os.path.join(os.path.dirname(__file__), "mlctl_init/model/__init__.py")))

        self.assertTrue(os.path.exists(
            os.path.join(project_path, "tests/__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(
            project_path, "tests/test_sample_project.py")))

        self.assertTrue(filecmp.cmp(os.path.join(project_path, ".gitignore"),
                                    os.path.join(os.path.dirname(__file__), "mlctl_init/.gitignore")))

        self.assertTrue(filecmp.cmp(os.path.join(project_path, "README.md"),
                                    os.path.join(os.path.dirname(__file__), "mlctl_init/README.md")))

        self.assertTrue(filecmp.cmp(os.path.join(project_path, "setup.cfg"),
                                    os.path.join(os.path.dirname(__file__), "mlctl_init/setup.cfg")))

        self.assertTrue(filecmp.cmp(os.path.join(project_path, "setup.py"),
                                    os.path.join(os.path.dirname(__file__), "mlctl_init/setup.py")))

        self.assertTrue(filecmp.cmp(os.path.join(project_path, "tox.ini"),
                                    os.path.join(os.path.dirname(__file__), "mlctl_init/tox.ini")))

        # removes model code from local directory
        rmtree(str(project_path))
