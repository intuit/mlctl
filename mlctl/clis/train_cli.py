import click
import os
from distutils.core import run_setup

from mlctl.clis.common.utils import determine_infra_plugin_from_job, parse_training_yamls, docker_instructions

@click.group(name='train', help="Train commands")
def train():
    pass


@train.command(name="build", help="build a container for training")
@click.option('--provider_config', '-p', envvar='PROVIDER_CONFIG', help="file location for the provider.yaml", metavar='')
@click.option('--config', '-c', required=True, help="config file containing parameters for training job", metavar='')
@click.option('--tag', '-t', help="Docker Image tag to save image to", metavar='')
def start(provider_config, config, tag):
    

    job = parse_training_yamls(config, provider_config)
    infrastructure_name = job.serialize()['infrastructure']['training']['name']

    # validate if there is a setup file to build from
    if not os.path.isfile('./setup.py'):
        print('Missing mlctl setup.py for building a mlctl universal container. \
        Try mlctl init, or navigating to the home directory of the project.')
        return
    click.echo("Building container for training job")
    
    # validate if there is a tag name, else use the default
    if tag:
        image_name = tag
    else:
        image_name = 'train-image'
    build = run_setup('./setup.py', 
        script_args=['sdist', '--dist-dir', './.mlctl','train',
        '-t', image_name,  '-p', infrastructure_name])
    click.echo(docker_instructions(image_name))
    return

@train.command(name="start", help="Train a model")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--provider_config', '-p', envvar='PROVIDER_CONFIG', help="file location for the provider.yaml", metavar='')
@click.option('--config', '-c', required=True, help="config file containing parameters for training job", metavar='')
def start(profile, provider_config, config):
    job = parse_training_yamls(config, provider_config)
    training = determine_infra_plugin_from_job(job, profile)
    click.echo(training.start_training(
        job))


@train.command(name="info", help="Get training job information")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--config', '-c', required=False, help="name of training job", metavar='')
@click.option('--training-job-name', '-t', required=False, help="name of training job", metavar='')
def info(profile, plugin, training_job_name, hyperparameter_tuning):
    training = determine_plugin(plugin, profile, 'training')
    click.echo(training.get_training_info(
        training_job_name, hyperparameter_tuning))


@train.command(name="stop", help="Stop a training job")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--training-job-name', '-t', required=True, help="name of training job", metavar='')
@click.option('--config', '-c', required=False, help="name of training job", metavar='')
def stop(profile, plugin, training_job_name, hyperparameter_tuning):
    training = determine_plugin(plugin, profile, 'training')

    click.echo(training.stop_training(
        training_job_name, hyperparameter_tuning))
