"""Fixtures which are included by default for Virtool workflows."""
from ..api.fixtures import *
from ..api.fixtures import __all__ as api_all
from ..config.fixtures import job_id, mem, proc, work_path
from ..execution.fixtures import run_in_executor, run_subprocess
from .workflow_fixture import fixture


@fixture
def results() -> dict:
    """
    The results dictionary.

    The value of this fixture will be attached to the analysis 
    record when the workflow completes successfully.
    """
    return {}


__all__ = [
    "job_id",
    "mem",
    "proc",
    "results",
    "run_in_executor",
    "run_subprocess",
    "work_path",
]

__all__.extend(api_all)
