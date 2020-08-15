import requests

TRELLO_ROOT = 'https://api.trello.com/1'


class Client(object):
    """Simple API connector"""

    def __init__(self, app_key, client_token):
        self.app_key = app_key
        self.client_token = client_token

    def url(self, endpoint, params=''):
        url = f'{TRELLO_ROOT}/{endpoint}?key={self.app_key}&token={self.client_token}'
        if params:
            url += f'&{params}'
        return url

    def get(self, endpoint, params=''):
        url = self.url(endpoint, params)
        response = requests.get(url)
        if response.status_code in [200, 300]:
            return response
        print(f'Error calling {endpoint} {params}')
        print(response, response.content)

    def post(self, endpoint, params=''):
        response = requests.post(self.url(endpoint, params))
        if response.status_code in [200, 300]:
            return response
        print(f'Error calling {endpoint} {params}')
        print(response, response.content)

    def put(self, endpoint, params=""):
        response = requests.put(self.url(endpoint, params))
        return response
