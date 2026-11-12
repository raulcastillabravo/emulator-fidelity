import gzip
import json
from pathlib import Path

from pipeline.aggregate import Aggregator
from pipeline.api_models import ApiModels
from pipeline.data_store import DataStore
from pipeline.git_source import GitSource
from pipeline.github import GitHub
from pipeline.manifest import Manifest


class ReleaseProcessor:
    _github: GitHub = None
    _store: DataStore = None
    _models_repo: GitSource = None
    _suite_repo: GitSource = None
    _cache: Path = None

    def __init__(self, github: GitHub, store: DataStore,
                 models_repo: GitSource, suite_repo: GitSource,
                 cache: Path):
        self._github = github
        self._store = store
        self._models_repo = models_repo
        self._suite_repo = suite_repo
        self._cache = cache

    def process(self, release: dict, latest: bool):
        published = release["published"]
        sources = {"api_models": self._models_repo.checkout_at(published),
                   "evaluation_suite": self._suite_repo.checkout_at(published)}
        models = ApiModels(self._models_repo.path).load()
        checks = Manifest(self._suite_repo.path / "manifest.jsonl").load()
        file = self._github.download_scores(release["tag"], self._cache)
        scores = json.loads(gzip.decompress(file.read_bytes()))
        result = Aggregator(models, checks).run(scores["units"])
        self._store.save_release({
            **release, "commit": scores["commit"],
            "scored_at": scores["scoredAt"], "sources": sources,
        }, result)
        if latest:
            self._store.save_latest(models, result, checks)
