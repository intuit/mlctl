import click
from mlctl.utils import determine_plugin


@click.group(name='hosting', help="Hosting commands")
def hosting():
    pass


@hosting.command(name="create", help="Create a model")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--model-config', '-c', required=True, help="config file containing model parameters", metavar='')
def create(profile, plugin, model_config):
    hosting = determine_plugin(plugin, profile, 'hosting')
    click.echo(hosting.create(model_config))


@hosting.command(name="deploy", help="Deploy a model")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--endpoint-name', '-e', required=True, help="name of endpoint", metavar='')
@click.option('--endpoint-config-name', '-ec', help="name of existing endpoint config", metavar='')
@click.option('--endpoint-config', '-c', help="config file containing parameters for endpoint config", metavar='')
@click.option('--tags', '-t', help="tags for endpoint", metavar='')
def deploy(profile, plugin, endpoint_name, endpoint_config_name, endpoint_config, tags):
    if endpoint_config_name and endpoint_config:
        raise click.BadOptionUsage("--endpoint-config-name / -ec",
                                   "Options '--endpoint-config-name / -ec' and '--endpoint-config / -c' cannot be used together.")
    hosting = determine_plugin(plugin, profile, 'hosting')
    click.echo(hosting.deploy(endpoint_name,
               endpoint_config_name, endpoint_config, tags))


@hosting.command(name="info", help="Get endpoint information")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--endpoint-name', '-e', required=True, help="name of endpoint", metavar='')
def info(profile, plugin, endpoint_name):
    hosting = determine_plugin(plugin, profile, 'hosting')
    click.echo(hosting.get_endpoint_info(endpoint_name))


@hosting.command(name="undeploy", help="Undeploy a model")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--endpoint-name', '-e',  help="name of endpoint", required=True, metavar='')
@click.option('--endpoint-config-name', '-c', help="name of endpoint config (include if you wish to delete the endpoint config of the endpoint)", metavar='')
def undeploy(profile, plugin, endpoint_name, endpoint_config_name):
    hosting = determine_plugin(plugin, profile, 'hosting')
    click.echo(hosting.undeploy(endpoint_name, endpoint_config_name))
