"""Meltano PipelineSerializer extension."""
from __future__ import annotations

import os
import pkgutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import structlog
from meltano.edk import models
from meltano.edk.extension import ExtensionBase
from meltano.edk.process import Invoker, log_subprocess_error

log = structlog.get_logger()


class PipelineSerializer(ExtensionBase):
    """Extension implementing the ExtensionBase interface."""

    def __init__(self) -> None:
        """Initialize the extension."""
        # TODO: Get environment name
        log.debug("Serializer initialized")

    def invoke(self, command_name: str | None, *command_args: Any) -> None:
        """Invoke the underlying cli, that is being wrapped by this extension.

        Args:
            command_name: The name of the command to invoke.
            command_args: The arguments to pass to the command.

        Raises:
            NotImplementedError: There is no underlying CLI for this extension.
        """
        raise NotImplementedError

    def describe(self) -> models.Describe:
        """Describe the extension.

        Returns:
            The extension description
        """
        # TODO: could we auto-generate all or portions of this from typer instead?
        return models.Describe(
            commands=[
                models.ExtensionCommand(
                    name="serializer", description="extension commands"
                )
            ]
        )

    def _get_lock_path(self, filename: str | None, filedir: str | None) -> None:
        lock_filename = filename or os.getenv("SERIALIZER_FILE_NAME", None) or "serializer.lck"
        lock_dir = filedir or os.getenv("SERIALIZER_DIR", None)  or "/tmp"
        return os.path.join(lock_dir, lock_filename)


    def acquire_lock(self, 
            filename: str = None,
            filedir: str = None,
            sleepseconds : int = None,
            maxattempts : int = None,
    ) -> None:
        lock_fullpath = self._get_lock_path(filename, filedir)

        log.info("Attempting to create lock file " + lock_fullpath)

        sleep_time_seconds = sleepseconds or int(os.getenv("SERIALIZER_SLEEP_SECONDS", 1))
        max_attempts = maxattempts or int(os.getenv("SERIALIZER_MAX_ATTEMPTS", 0))

        file_preexists = True
        num_waits = 0
        while file_preexists:
            try:
                with open(lock_fullpath, "x") as lckfl:
                    log.info("Created lock file")
                    file_preexists = False
            except FileExistsError:
                time.sleep(sleep_time_seconds)
                num_waits += 1

                if max_attempts > 0 and num_waits >= max_attempts:
                    log.info("Tried %s times totaling %s seconds" % (num_waits, num_waits * sleep_time_seconds))
                    raise

                if num_waits % 10 == 0:
                    log.info("Tried %s times totaling %s seconds" % (num_waits, num_waits * sleep_time_seconds))


    def release_lock(self, filename: str = None, filedir: str = None) -> None:
        lock_fullpath = self._get_lock_path(filename, filedir)

        log.info("Attempting to remove lock file " + lock_fullpath)

        os.remove(lock_fullpath)

        log.info("Removed lock file " + lock_fullpath)


