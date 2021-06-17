import click
from click.testing import CliRunner

from unittest import mock
import unittest

from mlctl.clis.hosting_cli import hosting


class TestHostingCli(unittest.TestCase):

    @mock.patch("mlctl.plugins.sagemaker.SagemakerHosting.SagemakerHosting.create")
    def test_create(self, mock_create):
        mock_create.return_value = "SagemakerHosting.create called"
        runner = CliRunner()
        response = runner.invoke(
            hosting, ["create", "-pl", "sagemaker", "-c", "model_config.json"])
        self.assertEqual(
            "SagemakerHosting.create called\n", response.output)
        mock_create.assert_called_with("model_config.json")

    @mock.patch("mlctl.plugins.sagemaker.SagemakerHosting.SagemakerHosting.deploy")
    def test_deploy(self, mock_deploy):
        mock_deploy.return_value = "SagemakerHosting.deploy called"
        runner = CliRunner()
        response = runner.invoke(
            hosting, ["deploy", "-pl", "sagemaker", "-e", "test-endpoint", "-c", "endpoint_config.json"])
        self.assertEqual(
            "SagemakerHosting.deploy called\n", response.output)
        mock_deploy.assert_called_with(
            "test-endpoint", None, "endpoint_config.json", None)

    @mock.patch("mlctl.plugins.sagemaker.SagemakerHosting.SagemakerHosting.deploy")
    def test_deploy_existing_config(self, mock_deploy):
        mock_deploy.return_value = "SagemakerHosting.deploy called with existing endpoint config"
        runner = CliRunner()
        response = runner.invoke(
            hosting, ["deploy", "-pl", "sagemaker", "-e", "test-endpoint", "-ec", "test-endpoint-config"])
        self.assertEqual(
            "SagemakerHosting.deploy called with existing endpoint config\n", response.output)
        mock_deploy.assert_called_with(
            "test-endpoint", "test-endpoint-config", None, None)

    @mock.patch("mlctl.plugins.sagemaker.SagemakerHosting.SagemakerHosting.deploy")
    def test_deploy_bad_option_error(self, mock_deploy):
        mock_deploy.return_value = "SagemakerHosting.deploy called with both endpoint config name and endpoint config file"
        runner = CliRunner()
        response = runner.invoke(
            hosting, ["deploy", "-pl", "sagemaker", "-e", "test-endpoint", "-ec", "test-endpoint-config", "-c", "endpoint_config.json"])
        self.assertIn(
            "Error: Options '--endpoint-config-name / -ec' and '--endpoint-config / -c' cannot be used together.", response.output)
        self.assertFalse(mock_deploy.called)

    @mock.patch("mlctl.plugins.sagemaker.SagemakerHosting.SagemakerHosting.undeploy")
    def test_undeploy(self, mock_undeploy):
        mock_undeploy.return_value = "SagemakerHosting.undeploy called"
        runner = CliRunner()
        response = runner.invoke(
            hosting, ["undeploy", "-pl", "sagemaker", "-e", "test-endpoint"])
        self.assertEqual(
            "SagemakerHosting.undeploy called\n", response.output)
        mock_undeploy.assert_called_with("test-endpoint", None)

    @mock.patch("mlctl.plugins.sagemaker.SagemakerHosting.SagemakerHosting.undeploy")
    def test_undeploy_delete_config(self, mock_undeploy):
        mock_undeploy.return_value = "SagemakerHosting.undeploy called with delete config"
        runner = CliRunner()
        response = runner.invoke(
            hosting, ["undeploy", "-pl", "sagemaker", "-e", "test-endpoint", "-c", "endpoint_config.json"])
        self.assertEqual(
            "SagemakerHosting.undeploy called with delete config\n", response.output)
        mock_undeploy.assert_called_with("test-endpoint", "endpoint_config.json")

    @mock.patch("mlctl.plugins.sagemaker.SagemakerHosting.SagemakerHosting.get_endpoint_info")
    def test_info(self, mock_info):
        mock_info.return_value = "SagemakerHosting.get_endpoint_info called"
        runner = CliRunner()
        response = runner.invoke(
            hosting, ["info", "-pl", "sagemaker", "-e", "test-endpoint"])
        self.assertEqual(
            "SagemakerHosting.get_endpoint_info called\n", response.output)
        mock_info.assert_called_with("test-endpoint")