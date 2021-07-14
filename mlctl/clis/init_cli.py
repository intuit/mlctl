import click
import os
from cookiecutter.main import cookiecutter

from mlctl.helpers.log_helper import Logger, enable_verbose_option


@click.command(name='init', help="Init command")
@click.option('--template', '-t', help="Location of the project template github location.", metavar='')
@enable_verbose_option()
def init(template, verbose):
    template_path = template if template else os.path.join(
        os.path.dirname(__file__), 'template')
    Logger.debug(
        f'Creating ML Model project using template from {template_path}')
    cookiecutter(template_path)
