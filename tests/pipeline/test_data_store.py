import json

from pipeline.aggregate import Aggregator
from pipeline.data_store import DataStore


def test_saves_release_summary(tmp_path, models, checks, units):
    store = DataStore(tmp_path)
    result = Aggregator(models, checks).run(units)

    store.save_release({"tag": "v1"}, result)

    saved = json.loads((tmp_path / "releases/v1.json").read_text())
    assert store.has("v1")
    assert saved["services"]["s3"] == {
        "total": [2, 3], "control": [1, 2], "data": [2, 2],
        "tested_ops": 2, "clean_ops": 1}


def test_saves_latest_catalog_and_details(tmp_path, models, checks,
                                          units):
    result = Aggregator(models, checks).run(units)

    DataStore(tmp_path).save_latest(models, result, checks)

    catalog = json.loads((tmp_path / "latest/catalog.json").read_text())
    s3 = json.loads((tmp_path / "latest/services/s3.json").read_text())
    assert [c["slug"] for c in catalog] == ["s3", "sqs"]
    assert s3["operations"]["DeleteBucket"] == [0, 0]
    assert s3["failing"] == [{"id": "s3.bad-name",
                              "path": "behavioral/s3/check_bad_name.py"}]
