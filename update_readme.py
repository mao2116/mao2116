#!/usr/bin/env python3
"""Auto-update README with compact GitHub stats."""

import os
import re
import json
import urllib.request
from urllib.parse import quote
from datetime import datetime, timezone

USERNAME = "mao2116"
README_PATH = "README.md"


def fetch_json(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "GitHub-README-Updater",
            "Accept": "application/vnd.github+json",
        },
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def get_github_stats():
    try:
        user_data = fetch_json(f"https://api.github.com/users/{USERNAME}")
        repos_data = fetch_json(
            f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"
        )

        return {
            "repos": user_data.get("public_repos", 0),
            "stars": sum(repo.get("stargazers_count", 0) for repo in repos_data),
            "followers": user_data.get("followers", 0),
            "following": user_data.get("following", 0),
        }

    except Exception as error:
        print(f"GitHub API error: {error}")
        return {
            "repos": "?",
            "stars": "?",
            "followers": "?",
            "following": "?",
        }


def shield_escape(value):
    text = str(value)
    text = text.replace("-", "--")
    text = text.replace("_", "__")
    return quote(text, safe="")


def build_stats_block(stats, now):
    repos = shield_escape(stats["repos"])
    stars = shield_escape(stats["stars"])
    followers = shield_escape(stats["followers"])
    following = shield_escape(stats["following"])
    updated = shield_escape(now)

    return f"""<!-- LIVE_STATS -->
<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=18&duration=2500&pause=700&color=00FF00&center=true&vCenter=true&width=560&height=38&lines=%E2%9A%A1+LIVE+GITHUB+STATS;%F0%9F%93%8A+AUTO+UPDATED;%F0%9F%94%A5+SYSTEM+ACTIVE" alt="Live GitHub Stats Animation">

  <br>

  <img src="https://img.shields.io/badge/Repos-{repos}-00ff00?style=flat-square&logo=github&logoColor=white&labelColor=0D1117" alt="Repos">
  <img src="https://img.shields.io/badge/Stars-{stars}-00ff00?style=flat-square&logo=github&logoColor=white&labelColor=0D1117" alt="Stars">
  <img src="https://img.shields.io/badge/Followers-{followers}-00ff00?style=flat-square&logo=githubsponsors&logoColor=white&labelColor=0D1117" alt="Followers">
  <img src="https://img.shields.io/badge/Following-{following}-00ff00?style=flat-square&logo=github&logoColor=white&labelColor=0D1117" alt="Following">
  <img src="https://img.shields.io/badge/Updated-{updated}-00ff00?style=flat-square&logo=clockify&logoColor=white&labelColor=0D1117" alt="Last Updated">
</div>
<!-- /LIVE_STATS -->"""


def update_readme():
    if not os.path.exists(README_PATH):
        raise FileNotFoundError("README.md not found in repository root.")

    with open(README_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    stats = get_github_stats()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    new_stats = build_stats_block(stats, now)

    if "<!-- LIVE_STATS -->" in content and "<!-- /LIVE_STATS -->" in content:
        content = re.sub(
            r"<!-- LIVE_STATS -->.*?<!-- /LIVE_STATS -->",
            new_stats,
            content,
            flags=re.DOTALL,
        )
    else:
        content += "\n\n## 📊 GitHub Live Stats\n\n" + new_stats + "\n"

    if "<!-- LAST_UPDATED -->" in content and "<!-- /LAST_UPDATED -->" in content:
        content = re.sub(
            r"<!-- LAST_UPDATED -->.*?<!-- /LAST_UPDATED -->",
            f"<!-- LAST_UPDATED -->{now}<!-- /LAST_UPDATED -->",
            content,
            flags=re.DOTALL,
        )
    else:
        content += f"\n\n<!-- LAST_UPDATED -->{now}<!-- /LAST_UPDATED -->\n"

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(content)

    print(
        f"✅ README updated | "
        f"Repos: {stats['repos']} | "
        f"Stars: {stats['stars']} | "
        f"Followers: {stats['followers']} | "
        f"Following: {stats['following']} | "
        f"Time: {now}"
    )


if __name__ == "__main__":
    update_readme()
