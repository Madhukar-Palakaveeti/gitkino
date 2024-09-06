import json

with open('new_repo_urls.json', 'r') as f:
    a = json.load(f)
arr = a['urls']
print(len(set(arr)))