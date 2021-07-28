import os
import click
from distutils.core import run_setup

from mlctl.clis.common.utils import determine_plugin
from mlctl.clis.common.utils import determine_infra_plugin_from_job, parse_hosting_yamls


@click.group(name='hosting', help="Hosting commands")
def hosting():
    pass


# @hosting.command(name="create", help="Create a model")
# @click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
# @click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
# @click.option('--model-config', '-c', required=True, help="config file containing model parameters", metavar='')
# def create(profile, plugin, model_config):
#     hosting = determine_plugin(plugin, profile, 'hosting')
#     click.echo(hosting.create(model_config))

@hosting.command(name="build", help="build a container for training")
@click.option('--provider_config', '-p', envvar='PROVIDER_CONFIG', help="file location for the provider.yaml", metavar='')
@click.option('--config', '-c', required=True, help="config file containing parameters for training job", metavar='')
@click.option('--tag', '-t', help="Docker Image tag to save image to", metavar='')
def start(provider_config, config, tag):
    
    job = parse_hosting_yamls(config, provider_config)
    infrastructure_name = job.serialize()['infrastructure']['hosting']['name']

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
        image_name = 'predict-image'
    build = run_setup('./setup.py', 
        script_args=['sdist', '--dist-dir', './.mlctl','predict',
        '-t', image_name,  '-p', infrastructure_name])
    click.echo(f'The container was built with tag {image_name}. \
To start the container on a service, tag your image to your remote repository and then push to it with the commands. For instance:\n\n\
docker tag {image_name} [remote_repository]\n\
docker push [remote_repository]')
    return

@hosting.command(name="start", help="Deploy a model to a hosting endpoint")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--provider_config', '-p', envvar='PROVIDER_CONFIG', help="file location for the provider.yaml", metavar='')
@click.option('--config', '-c', required=True, help="config file containing parameters for training job", metavar='')
def deploy(profile, provider_config, config):
    job = parse_hosting_yamls(config, provider_config)
    hosting = determine_infra_plugin_from_job(job, profile)
    hosting.create(job)
    click.echo(hosting.start_hosting(job))


@hosting.command(name="info", help="Get endpoint information")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--endpoint-name', '-e', required=True, help="name of endpoint", metavar='')
def info(profile, plugin, endpoint_name):
    hosting = determine_plugin(plugin, profile, 'hosting')
    click.echo(hosting.get_endpoint_info(endpoint_name))


@hosting.command(name="stop", help="Undeploy a model endpoint")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--endpoint-name', '-e',  help="name of endpoint", required=True, metavar='')
@click.option('--endpoint-config-name', '-c', help="name of endpoint config (include if you wish to delete the endpoint config of the endpoint)", metavar='')
def undeploy(profile, plugin, endpoint_name, endpoint_config_name):
    hosting = determine_plugin(plugin, profile, 'hosting')
    click.echo(hosting.stop_hosting(endpoint_name, endpoint_config_name))
