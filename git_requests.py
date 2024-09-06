import requests
import time 
import json
import os


access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
with open('repo_urls.json', 'r') as f:
    ob = json.load(f)
urls = ob['urls']

repo_num = 6001
while repo_num < 500000:
    main_url = f'https://api.github.com/repositories?since={repo_num}'
    response = requests.get(headers={'accept' : 'application/vnd.github+json', 
                                 'X-GitHub-Api-Version': '2022-11-28',
                                 'Authorization': f'Bearer {access_token}'
                                 }, 
                        url=main_url)
    if response.status_code == 200:
        batch_urls = []
        repos = response.json()
        for repo in repos:
            batch_urls.append(repo.get('url'))
        urls.extend(batch_urls)
        last_id = repos[-1].get('id')
    repo_num = last_id + 1

    time.sleep(1.5)
   
with open('new_repo_urls.json', 'w') as f:
    json.dump({'urls' : urls, 'last_id' : last_id}, f)


