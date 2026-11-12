import json
import shutil
from pathlib import Path


class DataStore:
    """Derived JSON files consumed by the website."""

    _root: Path = None

    def __init__(self, root: Path):
        self._root = root

    def has(self, tag: str) -> bool:
        return (self._root / "releases" / f"{tag}.json").exists()

    def save_release(self, release: dict, result: dict[str, dict]):
        services = {slug: {
            "total": s["total"], "control": s["control"],
            "data": s["data"], "tested_ops": len(s["ops"]),
            "clean_ops": sum(p == t for p, t in s["ops"].values()),
        } for slug, s in sorted(result.items())}
        self._write(f"releases/{release['tag']}.json",
                    {**release, "services": services})

    def save_latest(self, models: dict, result: dict, checks: dict):
        shutil.rmtree(self._root / "latest", ignore_errors=True)
        catalog = []
        for model in sorted(models.values(), key=lambda m: m["slug"]):
            stats = result.get(model["slug"])
            catalog.append({"slug": model["slug"], "title": model["title"],
                            "operations": len(model["operations"]),
                            "tested": stats is not None})
            if stats:
                self._write(f"latest/services/{model['slug']}.json",
                            _detail(model, stats, checks))
        self._write("latest/catalog.json", catalog)

    def _write(self, name: str, content: dict | list):
        file = self._root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(content, separators=(",", ":"))
        file.write_text(text + "\n")


def _detail(model: dict, stats: dict, checks: dict) -> dict:
    return {
        "slug": model["slug"], "title": model["title"],
        "operations": {op: stats["ops"].get(op, [0, 0])
                       for op in model["operations"]},
        "failing": [{"id": u, "path": checks.get(u, {}).get("path")}
                    for u in sorted(set(stats["failing"]))],
    }
