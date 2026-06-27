```python
#!/usr/bin/env python3
"""Auto-update README with live GitHub stats"""

import os
import re
import json
import urllib.request
from datetime import datetime, timezone

USERNAME = "mao2116"
README_PATH = "README.md"


def fetch_json(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/vnd.github+json",
    }

    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def get_stats():
    try:
        user_url = f"https://api.github.com/users/{USERNAME}"
        data = fetch_json(user_url)

        repos = data.get("public_repos", 0)
        followers = data.get("followers", 0)
        following = data.get("following", 0)

        repos_data = []
        page = 1

        while True:
            repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}"
            page_data = fetch_json(repos_url)

            if not isinstance(page_data, list) or not page_data:
                break

            repos_data.extend(page_data)

            if len(page_data) < 100:
                break

            page += 1

        stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)

        return {
            "repos": repos,
            "stars": stars,
            "followers": followers,
            "following": following,
        }

    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {
            "repos": "?",
            "stars": "?",
            "followers": "?",
            "following": "?",
        }


def make_row(label, value):
    inner_width = 38
    text = f"  {label:<12}: {value}"
    return f"│{text:<{inner_width}}│"


def make_stats_box(stats, now):
    title = "⚡ LIVE REALITY STATS"

    return f"""┌──────────────────────────────────────┐
│{title:^38}│
├──────────────────────────────────────┤
{make_row("📦 REPOS", stats["repos"])}
{make_row("⭐ STARS", stats["stars"])}
{make_row("👥 FOLLOWERS", stats["followers"])}
{make_row("👣 FOLLOWING", stats["following"])}
{make_row("⏰ UPDATED", now)}
└──────────────────────────────────────┘"""


def update():
    if not os.path.exists(README_PATH):
        print("README.md not found")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    stats = get_stats()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    new_stats = f"""<!-- LIVE_STATS -->
<pre>
{make_stats_box(stats, now)}
</pre>
<!-- /LIVE_STATS -->"""

    old_stats_pattern = r"<!-- LIVE_STATS -->[\s\S]*?<!-- /LIVE_STATS -->"

    if "<!-- LIVE_STATS -->" in content and "<!-- /LIVE_STATS -->" in content:
        content = re.sub(old_stats_pattern, new_stats, content, count=1)
    else:
        print("LIVE_STATS markers not found in README.md.")
        return

    new_ts = f"<!-- LAST_UPDATED -->{now}<!-- /LAST_UPDATED -->"
    old_ts_pattern = r"<!-- LAST_UPDATED -->[\s\S]*?<!-- /LAST_UPDATED -->"

    if "<!-- LAST_UPDATED -->" in content and "<!-- /LAST_UPDATED -->" in content:
        content = re.sub(old_ts_pattern, new_ts, content, count=1)
    else:
        print("LAST_UPDATED markers not found in README.md.")
        return

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(
        f"✅ Updated: {now} | "
        f"Repos: {stats['repos']} | "
        f"Stars: {stats['stars']} | "
        f"Followers: {stats['followers']} | "
        f"Following: {stats['following']}"
    )


if __name__ == "__main__":
    update()
```
