````python
#!/usr/bin/env python3
"""Auto-update README with live GitHub stats."""

import os
import re
import json
import urllib.request
from datetime import datetime, UTC

USERNAME = "mao2116"
README_PATH = "README.md"


def fetch_json(url: str):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/vnd.github+json",
        },
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def get_github_stats():
    try:
        user_url = f"https://api.github.com/users/{USERNAME}"
        repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"

        user_data = fetch_json(user_url)
        repos_data = fetch_json(repos_url)

        public_repos = user_data.get("public_repos", 0)
        followers = user_data.get("followers", 0)
        following = user_data.get("following", 0)
        stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)

        return {
            "repos": public_repos,
            "stars": stars,
            "followers": followers,
            "following": following,
        }

    except Exception as error:
        print(f"GitHub API error: {error}")
        return {
            "repos": "?",
            "stars": "?",
            "followers": "?",
            "following": "?",
        }


def build_stats_box(stats, now):
    return f"""<!-- LIVE_STATS -->
```text
┌──────────────────────────────────────┐
│       ⚡ LIVE REALITY STATS          │
├──────────────────────────────────────┤
│  📦 REPOS    : {str(stats["repos"]).rjust(22)} │
│  ⭐ STARS    : {str(stats["stars"]).rjust(22)} │
│  👥 FOLLOWERS: {str(stats["followers"]).rjust(22)} │
│  👣 FOLLOWING: {str(stats["following"]).rjust(22)} │
│  ⏰ UPDATED  : {now.ljust(22)} │
└──────────────────────────────────────┘
````

<!-- /LIVE_STATS -->"""

def update_readme():
if not os.path.exists(README_PATH):
print("README.md not found.")
return

```
with open(README_PATH, "r", encoding="utf-8") as file:
    content = file.read()

stats = get_github_stats()
now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

new_stats_block = build_stats_box(stats, now)

if "<!-- LIVE_STATS -->" in content and "<!-- /LIVE_STATS -->" in content:
    content = re.sub(
        r"<!-- LIVE_STATS -->.*?<!-- /LIVE_STATS -->",
        new_stats_block,
        content,
        flags=re.DOTALL,
    )

if "<!-- LAST_UPDATED -->" in content and "<!-- /LAST_UPDATED -->" in content:
    content = re.sub(
        r"<!-- LAST_UPDATED -->.*?<!-- /LAST_UPDATED -->",
        f"<!-- LAST_UPDATED -->{now}<!-- /LAST_UPDATED -->",
        content,
        flags=re.DOTALL,
    )

with open(README_PATH, "w", encoding="utf-8") as file:
    file.write(content)

print(
    f"Updated README: {now} | "
    f"Repos: {stats['repos']} | "
    f"Stars: {stats['stars']} | "
    f"Followers: {stats['followers']}"
)
```

if **name** == "**main**":
update_readme()

```
```
