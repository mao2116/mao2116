#!/usr/bin/env python3
"""Auto-update README with live GitHub stats"""

import os, re, random
from datetime import datetime
import urllib.request, json

def get_stats():
    try:
        url = "https://api.github.com/users/mao2116"
        req = urllib.request.urlopen(url, timeout=10)
        data = json.loads(req.read())
        
        repos = data.get("public_repos", "?")
        followers = data.get("followers", "?")
        following = data.get("following", "?")
        
        url2 = "https://api.github.com/users/mao2116/repos?per_page=100"
        req2 = urllib.request.urlopen(url2, timeout=10)
        repos_data = json.loads(req2.read())
        stars = sum(r.get("stargazers_count", 0) for r in repos_data)
        
        return {"repos": repos, "stars": stars, "followers": followers, "following": following}
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {"repos": "?", "stars": "?", "followers": "?", "following": "?"}

def update():
    path = "README.md"
    if not os.path.exists(path):
        print("README.md not found")
        return
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    stats = get_stats()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    # Ensure consistent width for the stats box
    # Adjust padding to accommodate larger numbers if needed
    new_stats = f"""<!-- LIVE_STATS -->
```
┌──────────────────────────────────────┐
│       ⚡ LIVE REALITY STATS          │
├──────────────────────────────────────┤
│  📦 REPOS    : {str(stats["repos"]).rjust(10)}         │
│  ⭐ STARS    : {str(stats["stars"]).rjust(10)}         │
│  👥 FOLLOWERS: {str(stats["followers"]).rjust(10)}         │
│  👣 FOLLOWING: {str(stats["following"]).rjust(10)}         │
│  ⏰ UPDATED  : {now}        │
└──────────────────────────────────────┘
```
<!-- /LIVE_STATS -->"""
    
    old_stats_pattern = r'<!-- LIVE_STATS -->.*?<!-- /LIVE_STATS -->'
    if '<!-- LIVE_STATS -->' in content:
        content = re.sub(old_stats_pattern, new_stats, content, flags=re.DOTALL)
    else:
        # If markers are not found, append to a logical place or add instructions
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
    
    print(f"✅ Updated: {now} | Repos: {stats['repos']} | Stars: {stats['stars']}")

update()
