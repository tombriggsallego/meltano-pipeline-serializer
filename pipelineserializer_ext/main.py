"""PipelineSerializer cli entrypoint."""

import os
import sys
from typing import List

import structlog
import typer
from meltano.edk.extension import DescribeFormat
from meltano.edk.logging import default_logging_config, parse_log_level
from pipelineserializer_ext.extension import PipelineSerializer

APP_NAME = "PipelineSerializer"

log = structlog.get_logger(APP_NAME)

ext = PipelineSerializer()

typer.core.rich = None  # remove to enable stylized help output when `rich` is installed
app = typer.Typer(
    name=APP_NAME,
    pretty_exceptions_enable=False,
)


@app.command()
def initialize(
    ctx: typer.Context,
    force: bool = typer.Option(False, help="Force initialization (if supported)"),
) -> None:
    """Initialize the PipelineSerializer plugin."""
    try:
        ext.initialize(force)
    except Exception:
        log.exception(
            "initialize failed with uncaught exception, please report to maintainer"
        )
        sys.exit(1)


@app.command(name="lock")
def acquire_command(
        filename : str = typer.Option(None, help="Name of the file to use for serialization"),
        filedir : str = typer.Option(None, help="Directory to store serialization file in"),
        sleepseconds : int = typer.Option(None, help="Number of seconds to sleep between checks if file exists"),
        maxattempts : int = typer.Option(None, help="Maximum number of times to try creating lock file"),
) -> None:
    """Acquire a lock to serialize around."""
    ext.acquire_lock(filename, filedir, sleepseconds, maxattempts)


@app.command(name="unlock")
def release_command(
        filename : str = typer.Option(None, help="Name of the file to use for serialization"),
        filedir : str = typer.Option(None, help="Directory to store serialization file in"),
) -> None:
    """Release a serialization lock."""
    ext.release_lock(filename, filedir)


@app.command()
def describe(
    output_format: DescribeFormat = typer.Option(
        DescribeFormat.text, "--format", help="Output format"
    )
) -> None:
    """Describe the available commands of this extension."""
    try:
        typer.echo(ext.describe_formatted(output_format))
    except Exception:
        log.exception(
            "describe failed with uncaught exception, please report to maintainer"
        )
        sys.exit(1)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    log_level: str = typer.Option("INFO", envvar="LOG_LEVEL"),
    log_timestamps: bool = typer.Option(
        False, envvar="LOG_TIMESTAMPS", help="Show timestamp in logs"
    ),
    log_levels: bool = typer.Option(
        False, "--log-levels", envvar="LOG_LEVELS", help="Show log levels"
    ),
    meltano_log_json: bool = typer.Option(
        False, "--meltano-log-json",
        envvar="MELTANO_LOG_JSON",
        help="Log in the meltano JSON log format"
    ),
) -> None:
    """Simple Meltano extension that serializes steps in a pipeline."""
    default_logging_config(
        level=parse_log_level(log_level),
        timestamps=log_timestamps,
        levels=log_levels,
        json_format=meltano_log_json
    )
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())

