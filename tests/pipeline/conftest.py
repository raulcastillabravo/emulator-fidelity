import json

import pytest


S3 = "com.amazonaws.s3#AmazonS3"
SQS = "com.amazonaws.sqs#AmazonSQS"


@pytest.fixture
def models() -> dict[str, dict]:
    return {
        S3: {"slug": "s3", "title": "Amazon S3",
             "operations": ["CreateBucket", "PutObject", "DeleteBucket"]},
        SQS: {"slug": "sqs", "title": "Amazon SQS",
              "operations": ["CreateQueue", "SendMessage"]},
    }


@pytest.fixture
def checks() -> dict[str, dict]:
    return {
        "s3.put": {"path": "behavioral/s3/check_put.py",
                   "planes": ["data"],
                   "operations": ["CreateBucket", "PutObject"]},
        "s3.bad-name": {"path": "behavioral/s3/check_bad_name.py",
                        "planes": ["control"],
                        "operations": ["CreateBucket"]},
        "s3__sqs.notify": {"path": "behavioral/s3__sqs/check_notify.py",
                           "planes": ["control", "data"],
                           "operations": ["CreateBucket", "SendMessage"]},
    }


@pytest.fixture
def units() -> list[dict]:
    def unit(unit_id, outcome, services, kind="behavioral"):
        return {"unitId": unit_id, "outcome": outcome, "kind": kind,
                "services": services}
    return [
        unit("s3.put", "pass", [S3]),
        unit("s3.bad-name", "fail", [S3]),
        unit("s3__sqs.notify", "pass", [S3, SQS]),
        unit("s3.wire", "fail", [S3], kind="wire"),
        unit("s3.skipped", "skipped", [S3]),
        unit("_smoke.unknown-service", "pass", ["com.amazonaws.x#X"]),
    ]


@pytest.fixture
def write_json():
    def write(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(content))
    return write
