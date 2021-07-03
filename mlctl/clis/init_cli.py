import click
from cookiecutter.main import cookiecutter


@click.command(name='init', help="init command")
@click.option('--template', '-t', help="Location of the project template github location.", metavar='')
def init(template):
    cookiecutter(template if template else 'template/')
