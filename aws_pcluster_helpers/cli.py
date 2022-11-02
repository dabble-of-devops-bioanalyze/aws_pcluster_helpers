import os

import typer

from aws_pcluster_helpers.commands import cli_sinfo
from aws_pcluster_helpers.commands import cli_gen_nxf_slurm_config

cli = typer.Typer()


@cli.command()
def sinfo(
    include_memory: bool = typer.Option(False, help="Include scheduleable memory"),
    scheduleable_memory: float = typer.Option(
        0.95, help="Schedulable amount of memory. Default is 95%"
    ),
):
    """
    A more helpful sinfo
    """
    print("Printing sinfo table")
    cli_sinfo.main()


@cli.command()
def gen_nxf_slurm_config(
    include_memory: bool = typer.Option(False, help="Include scheduleable memory"),
    scheduleable_memory: float = typer.Option(
        0.95, help="Schedulable amount of memory. Default is 95%"
    ),
    output: str = typer.Option(
        None, help="Path to nextflow slurm config file."
    ),
    overwrite: bool = typer.Option(False, help="Overwrite existing file."),
    stdout: bool = typer.Option(False, help="Write slurm config to stdout"),
):
    """
    Generate a slurm.config for nextflow that is compatible with your cluster.

    You will see a process label for each partition/node type.

    Use the configuration in your process by setting the label to match the label in the config.
    """
    print("Generating NXF Slurm config")
    cli_gen_nxf_slurm_config.main(
        output, overwrite, stdout, include_memory, scheduleable_memory
    )


if __name__ == "__main__":
    cli()
