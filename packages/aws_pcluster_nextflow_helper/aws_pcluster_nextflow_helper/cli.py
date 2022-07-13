"""Console script for aws_pcluster_nextflow_helper."""
import sys

import rich_click as click
from rich_click import RichCommand, RichGroup

from aws_pcluster_helpers.commands import cli_sinfo
from aws_pcluster_helpers.commands import cli_gen_nxf_slurm_config


@click.group()
def cli():
    """
    Helper functions for aws parallelcluster.
    """
    return


@cli.command()
def log():
    """
    A more helpful sinfo
    """
    click.echo("nextflow log")


if __name__ == "__main__":
    cli()
