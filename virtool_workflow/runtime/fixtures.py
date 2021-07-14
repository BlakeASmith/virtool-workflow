import logging
from .. import hooks
from ..fixtures.workflow_fixture import fixture
from ..fixtures import builtins as builtin_fixtures
from ..environment import WorkflowEnvironment
from ..fixtures.providers import ModuleFixtureGroup

logger = logging.getLogger(__name__)


@fixture
def environment(is_analysis_workflow: bool):
    if is_analysis_workflow:
        from ..analysis import fixtures as analysis_fixtures

        group = ModuleFixtureGroup(analysis_fixtures)

        @hooks.on_success
        async def upload_results(results, analysis_provider):
            logger.info("Uploading results...")
            await analysis_provider.upload_result(results)
            logger.info("Results uploaded")

        @hooks.on_failure
        async def delete(analysis_provider):
            await analysis_provider.delete()

    else:
        group = ModuleFixtureGroup(builtin_fixtures)

    return WorkflowEnvironment(group)
