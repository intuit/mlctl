import click
import os
from distutils.core import run_setup

from mlctl.clis.common.utils import determine_infra_plugin_from_job, parse_process_yamls, docker_instructions

@click.group(name='process', help="process commands")
def process():
    pass


@process.command(name="build", help="build a container for process")
@click.option('--provider_config', '-p', envvar='PROVIDER_CONFIG', help="file location for the provider.yaml", metavar='')
@click.option('--config', '-c', required=True, help="config file containing parameters for process job", metavar='')
@click.option('--tag', '-t', help="Docker Image tag to save image to", metavar='')
def start(provider_config, config, tag):
    

    job = parse_process_yamls(config, provider_config)
    infrastructure_name = job.serialize()['infrastructure']['process']['name']

    # validate if there is a setup file to build from
    if not os.path.isfile('./setup.py'):
        print('Missing mlctl setup.py for building a mlctl universal container. \
        Try mlctl init, or navigating to the home directory of the project.')
        return
    click.echo("Building container for process job")
    
    # validate if there is a tag name, else use the default
    if tag:
        image_name = tag
    else:
        image_name = 'process-image'
    build = run_setup('./setup.py', 
        script_args=['sdist', '--dist-dir', './.mlctl','process',
        '-t', image_name,  '-p', infrastructure_name])
    click.echo(docker_instructions(image_name))
    return

@process.command(name="start", help="process a model")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--provider_config', '-p', envvar='PROVIDER_CONFIG', help="file location for the provider.yaml", metavar='')
@click.option('--config', '-c', required=True, help="config file containing parameters for process job", metavar='')
def start(profile, provider_config, config):
    job = parse_process_yamls(config, provider_config)
    process = determine_infra_plugin_from_job(job, profile)
    click.echo(process.start_process(
        job))


@process.command(name="info", help="Get process job information")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--config', '-c', required=False, help="name of process job", metavar='')
@click.option('--process-job-name', '-t', required=False, help="name of process job", metavar='')
def info(profile, plugin, process_job_name, hyperparameter_tuning):
    # TODO: reimplement
    return

@process.command(name="stop", help="Stop a process job")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--process-job-name', '-t', required=True, help="name of process job", metavar='')
@click.option('--config', '-c', required=False, help="name of process job", metavar='')
def stop(profile, plugin, process_job_name, hyperparameter_tuning):
    # TODO: reimplement
    return