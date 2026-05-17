import os
import subprocess
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ORG_NAME = "lvncers-knowledge-base"
BASE_DIR = Path.home() / "knowledge-vault" / "repos"
TOKEN = os.getenv("GITHUB_TOKEN")

BASE_DIR.mkdir(parents=True, exist_ok=True)

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

repos = []
page = 1

while True:
    url = f"https://api.github.com/orgs/{ORG_NAME}/repos?per_page=100&page={page}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()

    if not data:
        break

    repos.extend(data)
    page += 1

print(f"Found {len(repos)} repositories")

for repo in repos:
    name = repo["name"]
    clone_url = repo["ssh_url"]

    target = BASE_DIR / name

    if target.exists():
        print(f"Updating {name}...")

        subprocess.run(
            ["git", "-C", str(target), "pull"],
            check=False
        )
    else:
        print(f"Cloning {name}...")

        subprocess.run(
            ["git", "clone", clone_url, str(target)],
            check=False
        )

print("Done")
