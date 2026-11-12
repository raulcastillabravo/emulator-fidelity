import json
from pathlib import Path


class Manifest:
    """Fidelity tests of aws/aws-emulator-evaluation-suite by check ID."""

    _file: Path = None

    def __init__(self, file: Path):
        self._file = file

    def load(self) -> dict[str, dict]:
        lines = self._file.read_text().splitlines()
        checks = (json.loads(line) for line in lines if line)
        return {c["check_id"]: {
            "path": c["path"],
            "planes": [label.split(":")[1] for label in c["labels"]
                       if label.startswith("plane:")],
            "operations": [o.split(":")[1] for o in c["operations"]],
        } for c in checks}
