import requests
import time 
import json
import os
import random

access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
HEADERS = {'accept' : 'application/vnd.github+json', 
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': f'Bearer {access_token}'
            }

urls = []

user_id = random.choice(range(10000))
max_id = user_id + 20000
while user_id < max_id:
    main_url = f'https://api.github.com/users?since={user_id}'
    response = requests.get(headers=HEADERS, url=main_url)
    if response.status_code == 200:
        batch_urls = []
        users = response.json()
        for user in users:
            user_url = user.get('url')
            repos_url = user.get('repos_url')
            batch_urls.append({'user_url' : user_url, 'repos_url' : repos_url})
        urls.extend(batch_urls)
        last_id = users[-1].get('id')
    user_id = last_id + 1

    time.sleep(0.5)
   
with open('user_urls.json', 'w') as f:
    json.dump({'urls' : urls, 'last_id' : last_id}, f)


