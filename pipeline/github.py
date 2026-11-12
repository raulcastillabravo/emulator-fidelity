import json
import subprocess
from pathlib import Path


ASSET = "scores.json.gz"


class GitHub:
    _repo: str = None

    def __init__(self, repo: str):
        self._repo = repo

    def releases_with_scores(self) -> list[dict]:
        """Releases that ship the scores asset, oldest first."""
        jq = (".[] | {tag: .tag_name, published: .published_at,"
              " assets: [.assets[].name]}")
        out = self._gh("api", "--paginate", "--jq", jq,
                       f"repos/{self._repo}/releases?per_page=100")
        releases = [json.loads(line) for line in out.splitlines()]
        found = [r for r in releases if ASSET in r.pop("assets")]
        return sorted(found, key=lambda r: r["published"])

    def download_scores(self, tag: str, folder: Path) -> Path:
        self._gh("release", "download", tag, "-R", self._repo,
                 "-p", ASSET, "-D", str(folder), "--clobber")
        return folder / ASSET

    def _gh(self, *args: str) -> str:
        return subprocess.run(["gh", *args], check=True,
                              capture_output=True, text=True).stdout
