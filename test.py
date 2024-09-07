import json
import requests
import os

# with open('user_urls.json', 'r') as f:
#     a = json.load(f)
# arr = a['urls']
access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
HEADERS = {'accept' : 'application/vnd.github+json', 
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': f'Bearer {access_token}'
            }
# url = 'https://api.github.com/users'
user_res = requests.get(headers=HEADERS,url='https://api.github.com/users/asyraf9')
repos_res = requests.get(headers=HEADERS,url='https://api.github.com/users/asyraf9/repos')
# if user_res.status_code == 200 and repos_res.status_code == 200:
#     batch_data = {}
#     user_data = user_res.json()
#     repos_data = repos_res.json()
#     batch_data['login'] = user_data['login']
#     batch_data['user_url'] = user_data['url']
#     batch_data['html_url'] =  user_data['html_url']
#     batch_data['repos_url'] =  user_data['repos_url']
#     batch_data['followers'] = user_data['followers']
#     batch_data['repo_details'] = [{'language' : repo['language'], 
#                                     'stars' : repo['stargazers_count'],
#                                     'forks' : repo['forks'],
#                                     'watchers' : repo['watchers']}
#                                     for repo in repos_data ]
    
print(repos_res.headers)