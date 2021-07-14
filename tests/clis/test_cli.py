import click
from click.testing import CliRunner

from unittest import mock
import unittest

from mlctl.clis.cli import _mlctl_pass_through


class TestCli(unittest.TestCase):

    def test_init(self):
        runner = CliRunner()
        response = runner.invoke(_mlctl_pass_through, ["init", "--help"])
        self.assertIn("Init command", response.output)

    def test_train(self):
        runner = CliRunner()
        response = runner.invoke(_mlctl_pass_through, "train")
        self.assertIn("Train commands", response.output)
    
    def test_batch(self):
        runner = CliRunner()
        response = runner.invoke(_mlctl_pass_through, "batch")
        self.assertIn("Batch inference commands", response.output)

    def test_hosting(self):
        runner = CliRunner()
        response = runner.invoke(_mlctl_pass_through, "hosting")
        self.assertIn("Hosting commands", response.output)
