from collections import defaultdict


class Aggregator:
    """Per-service fidelity of the behavioral tests of one release."""

    _models: dict[str, dict] = None
    _checks: dict[str, dict] = None

    def __init__(self, models: dict[str, dict], checks: dict[str, dict]):
        self._models = models
        self._checks = checks

    def run(self, units: list[dict]) -> dict[str, dict]:
        services = defaultdict(_empty)
        for unit in units:
            if unit["kind"] != "behavioral" or unit["outcome"] == "skipped":
                continue
            for shape_id in unit["services"]:
                if shape_id in self._models:
                    self._add(services[shape_id], shape_id, unit)
        return {self._models[s]["slug"]: v for s, v in services.items()}

    def _add(self, stats: dict, shape_id: str, unit: dict):
        passed = unit["outcome"] == "pass"
        check = self._checks.get(unit["unitId"], {})
        known = set(self._models[shape_id]["operations"])
        ops = known.intersection(check.get("operations", []))
        for counter in [stats["total"], *map(stats.get, check.get(
                "planes", [])), *(stats["ops"][op] for op in ops)]:
            counter[0] += passed
            counter[1] += 1
        if not passed:
            stats["failing"].append(unit["unitId"])


def _empty() -> dict:
    return {"total": [0, 0], "control": [0, 0], "data": [0, 0],
            "ops": defaultdict(lambda: [0, 0]), "failing": []}
