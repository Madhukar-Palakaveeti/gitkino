import os
import requests
import numpy as np

def language_count(garbage):
    top_tier_languages = {'Python','C', 'C++', 'JavaScript', 'TypeScript', 'Ruby', 'Rust', 'Lua', 'Assembly', 'Zig'}
    return len(garbage & top_tier_languages)

access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
HEADERS = {'accept' : 'application/vnd.github+json', 
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': f'Bearer {access_token}'
            }


class Layer_Dense:
  def __init__(self,n_inputs,n_neurons):
    self.weights = 0.01 * np.random.randn(n_inputs,n_neurons)
    self.biases = np.zeros((1,n_neurons))

  def forward(self,inputs):
    self.output = np.dot(inputs, self.weights)+ self.biases

  def parameters(self):
    return self.weights


class Activation_ReLU:
  def forward(self,inputs):
    self.output = np.maximum(0,inputs)

class Activation_Softmax:
  def forward(self,inputs):
    exp_values = np.exp(inputs - np.max(inputs,axis=1,keepdims=True))
    probabilities = exp_values/np.sum(exp_values,axis=1,keepdims=True)
    self.output = probabilities


class Loss_Categoricalcrossentropy():
  def forward(self, probs, y_true):
    probs_clipped = np.clip(probs, 1e-7, 1 - 1e-7)
    correct_confidences = np.sum(probs_clipped * y_true, axis=1)
    n_l_l = -np.log(correct_confidences)
    final_loss = np.mean(n_l_l)
    return final_loss


def get_user_data(user):
    user_url = f'https://api.github.com/users/{user}'
    repo_url = f'https://api.github.com/users/{user}/repos'
    user_res = requests.get(headers=HEADERS,url=user_url )
    repos_res = requests.get(headers=HEADERS,url=repo_url)
    if user_res.status_code == 200 and repos_res.status_code == 200:
        batch_data = {}
        user_data = user_res.json()
        repos_data = repos_res.json()
        batch_data['followers'] = user_data['followers']
        batch_data['languages'] = set()
        batch_data['total_stars'] = 0
        batch_data['total_forks'] = 0
        batch_data['kino_language_count'] = 0
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
            batch_data['repo_count'] = len(batch_data['repo_details'])
        batch_data['kino_language_count'] += language_count(batch_data['languages'])
        
    return [batch_data['followers'], batch_data['total_stars'], batch_data['total_forks'], batch_data['repo_count'], batch_data['kino_language_count']]

def predict(user_arr):
    layer1 = Layer_Dense(5,64)
    layer2 = Layer_Dense(64,64)
    layer3 = Layer_Dense(64,2)
    activation1 = Activation_ReLU()
    activation2 = Activation_ReLU()
    activation3 = Activation_Softmax()

    weights = np.load('resources/final_weights.npy', allow_pickle=True)
    layer1.weights = weights.item().get('w1')
    layer2.weights = weights.item().get('w2')
    layer3.weights = weights.item().get('w3')
    layer1.biases = weights.item().get('b1')
    layer2.biases = weights.item().get('b2')
    layer3.biases = weights.item().get('b3')


    layer1.forward(user_arr)
    activation1.forward(layer1.output)
    layer2.forward(activation1.output)
    activation2.forward(layer2.output)
    layer3.forward(activation2.output)
    activation3.forward(layer3.output)
    logits = activation3.output
    
    return np.argmax(logits)