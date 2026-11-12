import json

from pipeline.manifest import Manifest


def test_loads_checks_with_planes_and_operations(tmp_path):
    file = tmp_path / "manifest.jsonl"
    file.write_text(json.dumps({
        "check_id": "s3.put", "path": "behavioral/s3/check_put.py",
        "labels": ["axis:happy-path", "plane:control", "plane:data"],
        "operations": ["s3:CreateBucket", "s3:PutObject"],
    }) + "\n")

    checks = Manifest(file).load()

    assert checks == {"s3.put": {
        "path": "behavioral/s3/check_put.py",
        "planes": ["control", "data"],
        "operations": ["CreateBucket", "PutObject"]}}
