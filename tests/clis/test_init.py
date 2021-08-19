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

        template_path = os.path.join(os.path.dirname(__file__), '../../mlctl/clis/template/{{cookiecutter.package_name}}/')

        cmp = filecmp.dircmp(project_path, template_path)

        self.assertCountEqual(cmp.same_files, [".gitignore", "setup.cfg", "tox.ini"])
        self.assertCountEqual(cmp.common_dirs, ["model", "tests"])
        self.assertCountEqual(cmp.left_only, [])
        self.assertCountEqual(cmp.right_only, [])
        self.assertCountEqual(cmp.diff_files, ["README.md", "setup.py"])

        modeldircmp = filecmp.dircmp(os.path.join(project_path, "model"), os.path.join(template_path, "model"))

        self.assertCountEqual(modeldircmp.same_files, ["deploy.py", "process.py", "train.py"])
        self.assertCountEqual(modeldircmp.common_dirs, [])
        self.assertCountEqual(modeldircmp.left_only, [])
        self.assertCountEqual(modeldircmp.right_only, [])
        self.assertCountEqual(modeldircmp.diff_files, ["__init__.py"])

        testdircmp = filecmp.dircmp(os.path.join(project_path, "tests"), os.path.join(template_path, "tests"))

        self.assertCountEqual(testdircmp.same_files, [])
        self.assertCountEqual(testdircmp.common_dirs, [])
        self.assertCountEqual(testdircmp.left_only, ["test_sample_project.py"])
        self.assertCountEqual(testdircmp.right_only, ["test_{{cookiecutter.package_name.lower().replace(' ', '_').replace('-', '_')}}.py"])
        self.assertCountEqual(testdircmp.diff_files, ["__init__.py"])

        # TODO: test files that are different due to string replacement

        # clean up generated files, TODO: move to final
        rmtree(str(project_path))
