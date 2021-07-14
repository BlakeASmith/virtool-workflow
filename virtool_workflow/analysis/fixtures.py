"""Additional fixtures for Virtool analysis workflows."""
from typing import List

from .. import fixture
from ..api import (AnalysisProvider, HMMsProvider, IndexProvider,
                            SampleProvider, SubtractionProvider)
from ..errors import IllegalJobArguments, MissingJobArgument
from ..fixtures.builtins import *
from ..fixtures.builtins import __all__ as builtins_all
from .analysis import analysis
from .hmms import hmms
from .indexes import indexes
from .sample import sample
from .subtractions import subtractions


@fixture
def analysis_provider(job, http, jobs_api_url) -> AnalysisProvider:
    return AnalysisProvider(job.args["analysis_id"], http, jobs_api_url)


@fixture
def hmms_provider(http, jobs_api_url, work_path) -> HMMsProvider:
    return HMMsProvider(http, jobs_api_url, work_path)


@fixture
def index_provider(job, http, jobs_api_url) -> IndexProvider:
    try:
        return IndexProvider(job.args["index_id"], job.args["ref_id"], http, jobs_api_url)
    except KeyError as e:
        key = e.args[0]

        if key == "ref_id":
            raise IllegalJobArguments(
                f"Index {job.args['index_id']} given without 'ref_id'."
            )

        if key == "index_id":
            raise MissingJobArgument("Missing key 'index_id'")

        raise


@fixture
def sample_provider(job, http, jobs_api_url) -> SampleProvider:
    return SampleProvider(job.args["sample_id"], http, jobs_api_url)


@fixture
def subtraction_providers(
    job, http, jobs_api_url, work_path
) -> List[SubtractionProvider]:
    ids = job.args["subtraction_id"]
    if isinstance(ids, str) or isinstance(ids, bytes):
        ids = [ids]

    subtraction_work_path = work_path / "subtractions"
    subtraction_work_path.mkdir()

    return [
        SubtractionProvider(id_, http, jobs_api_url, subtraction_work_path)
        for id_ in ids
    ]

__all__ = [
    "analysis_provider",
    "analysis",
    "hmms_provider",
    "hmms",
    "index_provider",
    "indexes",
    "sample_provider",
    "sample",
    "subtraction_providers",
    "subtractions",
]

__all__.extend(builtins_all)
