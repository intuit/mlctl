import click
from mlctl.utils import determine_plugin
import os
import subprocess

@click.group(name='train', help="Train commands")
def train():
    pass

import sys
import time
@train.command(name="build", help="build a container for training")
def start():
    click.echo("Building container for training job")

    # TODO: make this a dynamic lookup
    if not os.path.isfile('./setup.py'):
        print('Missing mlctl setup.py for building a mlctl universal container. \
        Try mlctl init, or navigating to the home directory of the project.')
        return
    
    process = subprocess.Popen(['python3', './setup.py', 'train', '-t', 'train-image'],stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print (output.strip().decode())
    retval = process.poll()
    return

@train.command(name="push", help="push a container for training")
def start():

    # TODO:
    # Remove placeholder
    # check a state file for the container repo
    # tag the local image to the remote
    # push to the right repo
    click.echo("Pushing container for training job")
    def spinning_cursor():
        while True:
            for cursor in '|/-\\':
                yield cursor

    spinner = spinning_cursor()
    for _ in range(50):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
    

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
