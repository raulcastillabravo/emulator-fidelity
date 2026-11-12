from pipeline.aggregate import Aggregator


def test_counts_behavioral_tests_per_service(models, checks, units):
    result = Aggregator(models, checks).run(units)

    assert set(result) == {"s3", "sqs"}
    assert result["s3"]["total"] == [2, 3]
    assert result["sqs"]["total"] == [1, 1]


def test_counts_tests_in_every_plane_they_assert(models, checks, units):
    s3 = Aggregator(models, checks).run(units)["s3"]

    assert s3["control"] == [1, 2]
    assert s3["data"] == [2, 2]


def test_counts_tests_per_operation_of_the_service(models, checks, units):
    result = Aggregator(models, checks).run(units)

    assert dict(result["s3"]["ops"]) == {"CreateBucket": [2, 3],
                                         "PutObject": [1, 1]}
    assert dict(result["sqs"]["ops"]) == {"SendMessage": [1, 1]}


def test_lists_failing_tests(models, checks, units):
    result = Aggregator(models, checks).run(units)

    assert result["s3"]["failing"] == ["s3.bad-name"]
