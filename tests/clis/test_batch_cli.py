import click
from click.testing import CliRunner

from unittest import mock
import unittest

from mlctl.clis.batch_cli import batch


class TestBatchCli(unittest.TestCase):

    @mock.patch("mlctl.plugins.sagemaker.SagemakerBatch.SagemakerBatch.start_batch")
    def test_train(self, mock_start_batch):
        mock_start_batch.return_value = "SagemakerBatch.start_batch called"
        runner = CliRunner()
        response = runner.invoke(
            batch, ["start", "-pl", "sagemaker", "-c", "batch_config.json"])
        self.assertEqual(
            "SagemakerBatch.start_batch called\n", response.output)
        mock_start_batch.assert_called_with("batch_config.json")

    @mock.patch("mlctl.plugins.sagemaker.SagemakerBatch.SagemakerBatch.get_batch_info")
    def test_get_batch_info(self, mock_get_batch_info):
        mock_get_batch_info.return_value = "SagemakerBatch.get_batch_info called"
        runner = CliRunner()
        response = runner.invoke(
            batch, ["info", "-pl", "sagemaker", "-b", "test-batch-job"])
        self.assertEqual("SagemakerBatch.get_batch_info called\n", response.output)
        mock_get_batch_info.assert_called_with("test-batch-job")

    @mock.patch("mlctl.plugins.sagemaker.SagemakerBatch.SagemakerBatch.stop_batch")
    def test_stop(self, mock_stop_batch):
        mock_stop_batch.return_value = "SagemakerBatch.stop_batch called"
        runner = CliRunner()
        response = runner.invoke(
            batch, ["stop", "-pl", "sagemaker", "-b", "test-batch-job"])
        self.assertEqual("SagemakerBatch.stop_batch called\n", response.output)
        mock_stop_batch.assert_called_with("test-batch-job")
