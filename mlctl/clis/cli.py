import click
import mlctl
from mlctl.clis.init_cli import init
from mlctl.clis.train_cli import train
from mlctl.clis.deploy_cli import deploy
from mlctl.clis.batch_cli import batch
from mlctl.clis.process_cli import process


@click.group()
@click.version_option(mlctl.__version__)
def _mlctl_pass_through():
    pass


_mlctl_pass_through.add_command(init)
_mlctl_pass_through.add_command(train)
_mlctl_pass_through.add_command(batch)
_mlctl_pass_through.add_command(deploy)
_mlctl_pass_through.add_command(process)
