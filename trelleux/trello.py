import json
import requests

TRELLO_ROOT = "https://api.trello.com/1"

class Client(object):
    """Simple API connector"""

    def __init__(self, app_key, client_token):
        self.app_key = app_key
        self.client_token = client_token

    def url(self, endpoint, params=""):
        url = "{ROOT}/{endpoint}?key={APP_KEY}&token={TOKEN}".format(**{
            'ROOT': TRELLO_ROOT,
            'endpoint': endpoint,
            'TOKEN': self.client_token,
            'APP_KEY': self.app_key,
        })
        if params:
            url += "&%s" % params
        return url

    def get(self, endpoint, params=""):
        url = self.url(endpoint, params)
        response = requests.get(url)
        try:
            response.obj = json.loads(response.content)
        except Exception as e:
            print url
            print e
            pass
            # import pdb; pdb.set_trace()
        return response

    def post(self, endpoint, params=""):
        response = requests.post(self.url(endpoint, params))
        try:
            response.obj = json.loads(response.content)
        except Exception as e:
            print e
            pass
            # import pdb; pdb.set_trace()
        return response

    def put(self, endpoint, params=""):
        response = requests.put(self.url(endpoint, params))
        response.obj = json.loads(response.content)
        return response
