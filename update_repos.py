import requests
import os
import re

USERNAME = os.environ.get("GITHUB_USERNAME", "Greeshma-DS")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

# Fetch all public repos sorted by last pushed
url = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&direction=desc&per_page=6&type=public"
response = requests.get(url, headers=headers)
repos = response.json()

# Skip the profile repo itself
repos = [r for r in repos if r["name"] != USERNAME][:6]

# Build repo pin cards (2 per row using a table for alignment)
cards = []
for repo in repos:
    name = repo["name"]
    card = f'[![{name}](https://github-readme-stats.vercel.app/api/pin/?username={USERNAME}&repo={name}&theme=default&hide_border=true&border_radius=10&show_owner=false)](https://github.com/{USERNAME}/{name})'
    cards.append(card)

# Pair cards into rows of 2
rows = []
for i in range(0, len(cards), 2):
    pair = cards[i:i+2]
    rows.append("  " + "  \n  ".join(pair))

cards_md = "\n\n".join(rows)

inject = f"""<!-- REPOS_START -->
<div align="center">

{cards_md}

</div>
<!-- REPOS_END -->"""

# Read README
with open("README.md", "r") as f:
    content = f.read()

# Replace between markers
new_content = re.sub(
    r"<!-- REPOS_START -->.*?<!-- REPOS_END -->",
    inject,
    content,
    flags=re.DOTALL
)

with open("README.md", "w") as f:
    f.write(new_content)

print(f"✅ Injected {len(repos)} repos into README.md")
for r in repos:
    print(f"  - {r['name']} (pushed: {r['pushed_at']})")
