"""Fixtures relating to the Jobs API."""
from .. import fixture
from ..config.fixtures import jobs_api_url
from ..data_model import Job
from .client import authenticated_http, http
from .jobs import acquire_job, push_status


@fixture
async def job(job_id, acquire_job, scope) -> Job:
    job = await acquire_job(job_id)

    scope["http"] = await authenticated_http(job.id, job.key, scope["http"])

    return job


__all__ = [
    "http",
    "acquire_job",
    "push_status",
    "jobs_api_url",
    "job",
]
