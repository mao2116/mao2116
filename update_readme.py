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

```
token = os.getenv("GITHUB_TOKEN")
if token:
    headers["Authorization"] = f"Bearer {token}"

req = urllib.request.Request(url, headers=headers)

with urllib.request.urlopen(req, timeout=20) as response:
    return json.loads(response.read().decode("utf-8"))
```

def get_stats():
try:
user_data = fetch_json(f"https://api.github.com/users/{USERNAME}")

```
    repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)
    following = user_data.get("following", 0)

    repos_data = []
    page = 1

    while True:
        repo_page = fetch_json(
            f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}"
        )

        if not isinstance(repo_page, list) or not repo_page:
            break

        repos_data.extend(repo_page)

        if len(repo_page) < 100:
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
```

def make_row(label, value):
text = f"  {label:<12}: {value}"
return f"│{text:<38}│"

def make_stats_box(stats, now):
return f"""┌──────────────────────────────────────┐
│        ⚡ LIVE REALITY STATS         │
├──────────────────────────────────────┤
{make_row("📦 REPOS", stats["repos"])}
{make_row("⭐ STARS", stats["stars"])}
{make_row("👥 FOLLOWERS", stats["followers"])}
{make_row("👣 FOLLOWING", stats["following"])}
{make_row("⏰ UPDATED", now)}
└──────────────────────────────────────┘"""

def update():
if not os.path.exists(README_PATH):
raise FileNotFoundError("README.md not found")

```
with open(README_PATH, "r", encoding="utf-8") as file:
    content = file.read()

stats = get_stats()
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

new_stats = f"""<!-- LIVE_STATS -->
```

<pre>
{make_stats_box(stats, now)}
</pre>

<!-- /LIVE_STATS -->"""

```
if "<!-- LIVE_STATS -->" not in content or "<!-- /LIVE_STATS -->" not in content:
    raise ValueError("LIVE_STATS markers not found in README.md")

content = re.sub(
    r"<!-- LIVE_STATS -->[\s\S]*?<!-- /LIVE_STATS -->",
    new_stats,
    content,
    count=1,
)

new_timestamp = f"<!-- LAST_UPDATED -->{now}<!-- /LAST_UPDATED -->"

if "<!-- LAST_UPDATED -->" not in content or "<!-- /LAST_UPDATED -->" not in content:
    raise ValueError("LAST_UPDATED markers not found in README.md")

content = re.sub(
    r"<!-- LAST_UPDATED -->[\s\S]*?<!-- /LAST_UPDATED -->",
    new_timestamp,
    content,
    count=1,
)

with open(README_PATH, "w", encoding="utf-8") as file:
    file.write(content)

print(
    f"Updated: {now} | "
    f"Repos: {stats['repos']} | "
    f"Stars: {stats['stars']} | "
    f"Followers: {stats['followers']} | "
    f"Following: {stats['following']}"
)
```

if **name** == "**main**":
update()
