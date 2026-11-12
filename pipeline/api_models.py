import json
from pathlib import Path


class ApiModels:
    """Services of aws/api-models-aws, keyed by Smithy shape ID."""

    _root: Path = None

    def __init__(self, root: Path):
        self._root = root

    def load(self) -> dict[str, dict]:
        files = self._root.glob("models/*/service/*/*.json")
        return dict(self._service(f) for f in files)

    def _service(self, file: Path) -> tuple[str, dict]:
        shapes = json.loads(file.read_text())["shapes"]
        shape_id = next(k for k, v in shapes.items()
                        if v["type"] == "service")
        traits = shapes[shape_id].get("traits", {})
        sdk_id = traits.get("aws.api#service", {}).get("sdkId")
        slug = file.relative_to(self._root).parts[1]
        return shape_id, {
            "slug": slug,
            "title": traits.get("smithy.api#title") or sdk_id or slug,
            "operations": sorted(k.split("#")[1] for k, v in shapes.items()
                                 if v["type"] == "operation"),
        }
