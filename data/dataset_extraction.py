import requests
import time
import os
import json
import numpy as np

data = []
access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
HEADERS = {'accept' : 'application/vnd.github+json', 
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': f'Bearer {access_token}'
          }
with open('user_urls.json', 'r') as f:
    ob = json.load(f)

full_urls = ob['urls']
full_urls = full_urls[:5000]
urls = np.random.choice(full_urls, size=2500, replace=False)
for url in urls:
    user_url = url['user_url']
    repos_url = url['repos_url']
    user_res = requests.get(headers=HEADERS,url=user_url)
    repos_res = requests.get(headers=HEADERS,url=repos_url)
    if user_res.status_code == 200 and repos_res.status_code == 200:
        batch_data = {}
        user_data = user_res.json()
        repos_data = repos_res.json()
        batch_data['login'] = user_data['login']
        batch_data['user_url'] = user_data['url']
        batch_data['html_url'] =  user_data['html_url']
        batch_data['repos_url'] =  user_data['repos_url']
        batch_data['followers'] = user_data['followers']
        batch_data['repo_details'] = [{'language' : repo['language'], 
                                       'stars' : repo['stargazers_count'],
                                       'forks' : repo['forks'],
                                       'watchers' : repo['watchers']}
                                     for repo in repos_data ]
        data.append(batch_data)
    time.sleep(1.5)

with open('dataset.json' , 'w') as f:
    json.dump({'data' : data}, f)