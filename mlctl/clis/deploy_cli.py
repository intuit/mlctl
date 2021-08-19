import os
import click
from distutils.core import run_setup

from mlctl.clis.common.utils import determine_infra_plugin_from_job, parse_deploy_yamls, docker_instructions


@click.group(name='deploy', help="deploy commands")
def deploy():
    pass


# @deploy.command(name="create", help="Create a model")
# @click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
# @click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
# @click.option('--model-config', '-c', required=True, help="config file containing model parameters", metavar='')
# def create(profile, plugin, model_config):
#     deploy = determine_plugin(plugin, profile, 'deploy')
#     click.echo(deploy.create(model_config))

@deploy.command(name="build", help="build a container for training")
@click.option('--provider_config', '-p', envvar='PROVIDER_CONFIG', help="file location for the provider.yaml", metavar='')
@click.option('--config', '-c', required=True, help="config file containing parameters for training job", metavar='')
@click.option('--tag', '-t', help="Docker Image tag to save image to", metavar='')
def build(provider_config, config, tag):
    
    job = parse_deploy_yamls(config, provider_config)
    infrastructure_name = job.serialize()['infrastructure']['deploy']['name']

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
        image_name = 'deploy-image'
    build = run_setup('./setup.py', 
        script_args=['sdist', '--dist-dir', './.mlctl','deploy',
        '-t', image_name,  '-p', infrastructure_name])
    click.echo(docker_instructions(image_name))
    return

@deploy.command(name="start", help="Deploy a model to a deploy endpoint")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--provider_config', '-p', envvar='PROVIDER_CONFIG', help="file location for the provider.yaml", metavar='')
@click.option('--config', '-c', required=True, help="config file containing parameters for training job", metavar='')
def start(profile, provider_config, config):
    job = parse_deploy_yamls(config, provider_config)
    deploy_job = determine_infra_plugin_from_job(job, profile)
    deploy_job.create(job)
    click.echo(deploy_job.start_deploy(job))
    return

@deploy.command(name="info", help="Get endpoint information")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--endpoint-name', '-e', required=True, help="name of endpoint", metavar='')
def info(profile, plugin, endpoint_name):
    # TODO: reimplement
    return


@deploy.command(name="stop", help="Undeploy a model endpoint")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--endpoint-name', '-e',  help="name of endpoint", required=True, metavar='')
@click.option('--endpoint-config-name', '-c', help="name of endpoint config (include if you wish to delete the endpoint config of the endpoint)", metavar='')
def undeploy(profile, plugin, endpoint_name, endpoint_config_name):
    # TODO: reimplement
    return