from pathlib import Path

from pipeline.data_store import DataStore
from pipeline.git_source import GitSource
from pipeline.github import GitHub
from pipeline.release_processor import ReleaseProcessor


ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache"
GITHUB = "https://github.com/aws"


def main():
    github = GitHub("aws/aws-emulator")
    store = DataStore(ROOT / "data")
    processor = ReleaseProcessor(
        github, store,
        GitSource(f"{GITHUB}/api-models-aws.git", CACHE / "api-models-aws",
                  "models"),
        GitSource(f"{GITHUB}/aws-emulator-evaluation-suite.git",
                  CACHE / "evaluation-suite", "manifest.jsonl"),
        CACHE)
    releases = github.releases_with_scores()
    for release in releases:
        if not store.has(release["tag"]):
            print(f"Processing {release['tag']}")
            processor.process(release, latest=release is releases[-1])


if __name__ == "__main__":
    main()
