import click
from click.testing import CliRunner
from unittest import mock
import unittest
from mlctl.clis.train_cli import train


class TestTrainCli(unittest.TestCase):

    @mock.patch("mlctl.plugins.sagemaker.SagemakerTraining.SagemakerTraining.start_training")
    def test_train(self, mock_start_training):
        mock_start_training.return_value = "SagemakerTraining.start_training called"
        runner = CliRunner()
        response = runner.invoke(
            train, ["start", "-pl", "sagemaker", "-c", "training_config.json"])
        self.assertEqual(
            "SagemakerTraining.start_training called\n", response.output)
        mock_start_training.assert_called_with("training_config.json", False)

    @mock.patch("mlctl.plugins.sagemaker.SagemakerTraining.SagemakerTraining.start_training")
    def test_train_tuning(self, mock_start_training):
        mock_start_training.return_value = "SagemakerTraining.start_training called"
        runner = CliRunner()
        response = runner.invoke(train, [
                                 "start", "-pl", "sagemaker", "-c", "training_config.json", "--hyperparameter-tuning"])
        self.assertEqual(
            "SagemakerTraining.start_training called\n", response.output)
        mock_start_training.assert_called_with("training_config.json", True)

    @mock.patch("mlctl.plugins.sagemaker.SagemakerTraining.SagemakerTraining.get_training_info")
    def test_get_training_info(self, mock_get_training_info):
        mock_get_training_info.return_value = "SagemakerTraining.get_training_info called"
        runner = CliRunner()
        response = runner.invoke(
            train, ["info", "-pl", "sagemaker", "-t", "test-training-job"])
        self.assertEqual(
            "SagemakerTraining.get_training_info called\n", response.output)
        mock_get_training_info.assert_called_with("test-training-job", False)

    @mock.patch("mlctl.plugins.sagemaker.SagemakerTraining.SagemakerTraining.get_training_info")
    def test_get_training_info_tuning(self, mock_get_training_info):
        mock_get_training_info.return_value = "SagemakerTraining.get_training_info called"
        runner = CliRunner()
        response = runner.invoke(train, [
                                 "info", "-pl", "sagemaker", "-t", "test-training-job", "--hyperparameter-tuning"])
        self.assertEqual(
            "SagemakerTraining.get_training_info called\n", response.output)
        mock_get_training_info.assert_called_with("test-training-job", True)

    @mock.patch("mlctl.plugins.sagemaker.SagemakerTraining.SagemakerTraining.stop_training")
    def test_stop(self, mock_stop_training):
        mock_stop_training.return_value = "SagemakerTraining.stop_training called"
        runner = CliRunner()
        response = runner.invoke(
            train, ["stop", "-pl", "sagemaker", "-t", "test-training-job"])
        self.assertEqual(
            "SagemakerTraining.stop_training called\n", response.output)
        mock_stop_training.assert_called_with("test-training-job", False)

    @mock.patch("mlctl.plugins.sagemaker.SagemakerTraining.SagemakerTraining.stop_training")
    def test_stop_tuning(self, mock_stop_training):
        mock_stop_training.return_value = "SagemakerTraining.stop_training called"
        runner = CliRunner()
        response = runner.invoke(train, [
                                 "stop", "-pl", "sagemaker", "-t", "test-training-job", "--hyperparameter-tuning"])
        self.assertEqual(
            "SagemakerTraining.stop_training called\n", response.output)
        mock_stop_training.assert_called_with("test-training-job", True)
