import json
import requests
import os



def language_count(garbage):
    top_tier_languages = {'Python','C', 'C++', 'JavaScript', 'TypeScript', 'Ruby', 'Rust', 'Lua', 'Assembly', 'Zig'}
    return len(garbage & top_tier_languages)

# # with open('user_urls.json', 'r') as f:
# #     a = json.load(f)
# # arr = a['urls']
access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
HEADERS = {'accept' : 'application/vnd.github+json', 
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': f'Bearer {access_token}'
            }
# # url = 'https://api.github.com/users'
user_res = requests.get(headers=HEADERS,url='https://api.github.com/users/yacineMTB' )
repos_res = requests.get(headers=HEADERS,url='https://api.github.com/users/yacineMTB/repos')
if user_res.status_code == 200 and repos_res.status_code == 200:
    batch_data = {}
    user_data = user_res.json()
    repos_data = repos_res.json()
    # batch_data['login'] = user_data['login']
    # batch_data['user_url'] = user_data['url']
    # batch_data['html_url'] =  user_data['html_url']
    # batch_data['repos_url'] =  user_data['repos_url']
    batch_data['followers'] = user_data['followers']
    batch_data['languages'] = set()
    batch_data['total_stars'] = 0
    batch_data['total_forks'] = 0
    batch_data['kino_language_count'] = 0
    # batch_data['total_watchers'] = 0
    batch_data['repo_details'] = [{'language' : repo['language'], 
                                    'stars' : repo['stargazers_count'],
                                    'forks' : repo['forks'],
                                    'watchers' : repo['watchers']}
                                    for repo in repos_data ]
    
    for repo in batch_data['repo_details']:
        if repo['language'] is not None:
            batch_data['languages'].add(repo['language'])
        batch_data['total_stars'] += repo['stars']
        batch_data['total_forks'] += repo['forks']
        # batch_data['total_watchers'] += repo['watchers']
        batch_data['repo_count'] = len(batch_data['repo_details'])
    batch_data['kino_language_count'] += language_count(batch_data['languages'])
    
print([batch_data['followers'], batch_data['total_stars'], batch_data['total_forks'], batch_data['repo_count'], batch_data['kino_language_count']])
# with open('resources/dataset.json', 'r') as f:
#     d = json.load(f)
# data = d['data']
# print(data[1])
# with open('resources/user_urls.json', 'r') as f:
#     ob = json.load(f)
# print(ob['last_id'])