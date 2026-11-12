import subprocess
from pathlib import Path


class GitSource:
    """Blobless, sparse clone of a Git repo, checked out by date."""

    path: Path = None
    _url: str = None
    _content: str = None

    def __init__(self, url: str, path: Path, content: str):
        """content: path holding the data, e.g. "models"."""
        self.path = path
        self._url = url
        self._content = content

    def checkout_at(self, timestamp: str) -> str:
        """Check out the content as it was at an ISO timestamp.

        Falls back to the oldest version when it did not exist yet.
        """
        if not self.path.exists():
            self._run("git", "clone", "--filter=blob:none",
                      "--no-checkout", self._url, str(self.path))
            self._git("sparse-checkout", "set", "--no-cone",
                      f"/{self._content}")
        self._git("fetch", "--quiet", "origin")
        path = ["origin/HEAD", "--", self._content]
        before = self._git("log", "--format=%H", "-1",
                           f"--before={timestamp}", *path)
        oldest = "log", "--format=%H", "--reverse", *path
        sha = before.strip() or self._git(*oldest).split()[0]
        self._git("checkout", "--quiet", "--detach", sha)
        return sha

    def _git(self, *args: str) -> str:
        return self._run("git", "-C", str(self.path), *args)

    def _run(self, *cmd: str) -> str:
        return subprocess.run(cmd, check=True, capture_output=True,
                              text=True).stdout
