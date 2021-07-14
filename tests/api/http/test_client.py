import pytest
from tests.api.mocks.mock_job_routes import TEST_JOB
from virtool_workflow import FixtureScope
from virtool_workflow.api import fixtures as api_fixtures
from virtool_workflow.api.client import JobApiHttpSession, authenticated_http
from virtool_workflow.fixtures import builtins
from virtool_workflow.fixtures.providers import ModuleFixtureGroup
from virtool_workflow.fixtures.scope import FixtureScope


@pytest.fixture
async def api_scope():
    async with FixtureScope(ModuleFixtureGroup(api_fixtures), ModuleFixtureGroup(builtins)) as scope:
        yield scope



@pytest.fixture
async def client(api_scope):
    return await api_scope.get_or_instantiate("http")


async def test_http_client_does_close(client, api_scope):
    assert isinstance(client, JobApiHttpSession)

    await api_scope.close()

    assert client.client.closed


async def test_add_auth_headers_adds_auth(api_scope):
    job_id = "test_job"
    job_key = "foobar"

    api_scope["job_id"] = job_id
    api_scope["key"] = job_key

    client = await api_scope.instantiate(authenticated_http)

    assert client.auth.login == f"job-{job_id}"
    assert client.auth.password == job_key


async def test_auth_headers_applied_once_job_is_ready(http, jobs_api_url, api_scope):
    api_scope["http"] = http
    api_scope["job_id"] = TEST_JOB["id"]
    api_scope["jobs_api_url"] = jobs_api_url
    job = await api_scope.get_or_instantiate("job")

    assert http.auth.login == f"job-{job.id}"
    assert http.auth.password == job.key
