
#!/usr/bin/env python3
"""Auto-update README with live GitHub stats"""

import os, re, random
from datetime import datetime, UTC
import urllib.request, json

def get_github_stats():
    try:
        url = "https://api.github.com/users/mao2116"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
        
        repos = data.get("public_repos", 0)
        followers = data.get("followers", 0)
        following = data.get("following", 0)
        
        url2 = "https://api.github.com/users/mao2116/repos?per_page=100"
        req2 = urllib.request.Request(url2, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        with urllib.request.urlopen(req2, timeout=10) as response2:
            repos_data = json.loads(response2.read())
        stars = sum(r.get("stargazers_count", 0) for r in repos_data)
        
        return {"repos": repos, "stars": stars, "followers": followers, "following": following}
    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")
        return {"repos": "?", "stars": "?", "followers": "?", "following": "?"}

def update_readme():
    path = "README.md"
    if not os.path.exists(path):
        print("README.md not found")
        return
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    github_stats = get_github_stats()
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    
    # Define a fixed width for the stats box content area for perfect alignment
    content_width = 25 # This is the width for the actual data part, e.g., '     ?' or '    123'
    box_width = 40 # Total width of the ASCII box

    # Format stats with dynamic padding to ensure alignment
    repos_str = str(github_stats["repos"]).rjust(content_width)
    stars_str = str(github_stats["stars"]).rjust(content_width)
    followers_str = str(github_stats["followers"]).rjust(content_width)
    following_str = str(github_stats["following"]).rjust(content_width)
    updated_str = now.ljust(content_width)

    new_stats = f"""<!-- LIVE_STATS -->
```
┌──────────────────────────────────────┐
│       ⚡ LIVE REALITY STATS          │
├──────────────────────────────────────┤
│  📦 REPOS    : {repos_str} │
│  ⭐ STARS    : {stars_str} │
│  👥 FOLLOWERS: {followers_str} │
│  👣 FOLLOWING: {following_str} │
│  ⏰ UPDATED  : {updated_str} │
└──────────────────────────────────────┘
```
<!-- /LIVE_STATS -->"""
    
    old_stats_pattern = r'<!-- LIVE_STATS -->.*?<!-- /LIVE_STATS -->'
    if '<!-- LIVE_STATS -->' in content:
        content = re.sub(old_stats_pattern, new_stats, content, flags=re.DOTALL)
    else:
        print("LIVE_STATS markers not found in README.md. Please ensure they are present.")
        return
    
    old_ts_pattern = r'<!-- LAST_UPDATED -->.*?<!-- /LAST_UPDATED -->'
    new_ts = f'<!-- LAST_UPDATED -->{now}<!-- /LAST_UPDATED -->'
    if '<!-- LAST_UPDATED -->' in content:
        content = re.sub(old_ts_pattern, new_ts, content, flags=re.DOTALL)
    else:
        print("LAST_UPDATED markers not found in README.md. Please ensure they are present.")
        return
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Updated: {now} | Repos: {github_stats['repos']} | Stars: {github_stats['stars']}")

update_readme()
