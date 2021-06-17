import click
from mlctl.utils import determine_plugin


@click.group(name='batch', help="Batch inference commands")
def batch():
    pass


@batch.command(name="start", help="Trigger a batch inference job")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--config', '-c', required=True, help="config file containing batch inference job parameters", metavar='')
def start(profile, plugin, config):
    batch = determine_plugin(plugin, profile, 'batch')
    click.echo(batch.start_batch(config))


@batch.command(name="info", help="Get batch inference job information")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--batch_job_name', '-b', required=True, help="name of batch inference job", metavar='')
def info(profile, plugin, batch_job_name):
    batch = determine_plugin(plugin, profile, 'batch')
    click.echo(batch.get_batch_info(
        batch_job_name))


@batch.command(name="stop", help="Stop a batch inference job")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--plugin', '-pl', envvar='PLUGIN', help="plugin (i.e. sagemaker, azure)", metavar='', type=click.Choice(['sagemaker']), required=True)
@click.option('--batch_job_name', '-b', required=True, help="name of batch inference job", metavar='')
def stop(profile, plugin, batch_job_name):
    batch = determine_plugin(plugin, profile, 'batch')
    click.echo(batch.stop_batch(batch_job_name))
