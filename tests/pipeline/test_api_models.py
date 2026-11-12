from pipeline.api_models import ApiModels


def test_loads_services_by_shape_id(tmp_path, write_json):
    write_json(tmp_path / "models/s3/service/2006-03-01/s3.json", {
        "shapes": {
            "com.amazonaws.s3#AmazonS3": {"type": "service", "traits": {
                "smithy.api#title": "Amazon Simple Storage Service"}},
            "com.amazonaws.s3#PutObject": {"type": "operation"},
            "com.amazonaws.s3#Bucket": {"type": "structure"},
        }})

    models = ApiModels(tmp_path).load()

    assert models == {"com.amazonaws.s3#AmazonS3": {
        "slug": "s3", "title": "Amazon Simple Storage Service",
        "operations": ["PutObject"]}}
