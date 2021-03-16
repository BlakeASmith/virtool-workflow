"""Main entrypoint(s) to run virtool workflows."""
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from virtool_workflow import discovery, FixtureScope
from virtool_workflow.config.configuration import load_config, config_fixtures
from virtool_workflow.hooks import on_load_config
from virtool_workflow.runtime import fixtures

logger = logging.getLogger(__name__)


@on_load_config
def set_log_level_to_debug(dev_mode: bool):
    if dev_mode:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


@on_load_config
def load_scripts(init_file: Path, fixtures_file: Path):
    if init_file.exists():
        discovery.import_module_from_file(module_name=init_file.name.rstrip(".py"), path=init_file)
    if fixtures_file.exists():
        discovery.import_module_from_file(module_name=fixtures_file.name.rstrip(".py"), path=fixtures_file)


@on_load_config
def extract_workflow(workflow_file_path: Path, scope):
    _workflow = discovery.discover_workflow(workflow_file_path)
    if not _workflow:
        raise RuntimeError(f"{workflow_file_path.name} does not contain a Workflow.")

    scope["workflow"] = _workflow


@asynccontextmanager
async def prepare_environment(**config):
    scope = FixtureScope(config_fixtures)
    await load_config(scope=scope, **config)
    scope.add_provider(fixtures.runtime)

    environment = await scope.get_or_instantiate("environment")
    workflow = scope["workflow"]

    async with environment:
        yield environment, workflow


async def start(**config):
    async with prepare_environment(**config) as (environment, workflow):
        await environment.execute(workflow)