import click
import os
from cookiecutter.main import cookiecutter


@click.command(name='init', help="init command")
@click.option('--template', '-t', help="Location of the project template github location.", metavar='')
def init(template):
    template_path = template if template else os.path.join(
        os.path.dirname(__file__), 'template')
    cookiecutter(template_path)
