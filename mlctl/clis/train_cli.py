import click
from mlctl.utils import determine_plugin


@click.group(name='train', help="Train commands")
def train():
    pass


@train.command(name="start", help="Train a model")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--hyperparameter-tuning', is_flag=True, help="indicates that training job performs hyperparameter-tuning", metavar='')
@click.option('--config', '-c', required=True, help="config file containing parameters for training job", metavar='')
def start(profile, plugin, hyperparameter_tuning, config):
    training = determine_plugin(plugin, profile, 'training')
    click.echo(training.start_training(
        config, hyperparameter_tuning))


@train.command(name="info", help="Get training job information")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--training-job-name', '-t', required=True, help="name of training job", metavar='')
@click.option('--hyperparameter-tuning', is_flag=True, help="indicates that training job performs hyperparameter-tuning", metavar='')
def info(profile, plugin, training_job_name, hyperparameter_tuning):
    training = determine_plugin(plugin, profile, 'training')
    click.echo(training.get_training_info(
        training_job_name, hyperparameter_tuning))


@train.command(name="stop", help="Stop a training job")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--training-job-name', '-t', required=True, help="name of training job", metavar='')
@click.option('--hyperparameter-tuning', is_flag=True, help="indicates that training job performs hyperparameter-tuning", metavar='')
def stop(profile, plugin, training_job_name, hyperparameter_tuning):
    training = determine_plugin(plugin, profile, 'training')

    click.echo(training.stop_training(
        training_job_name, hyperparameter_tuning))
