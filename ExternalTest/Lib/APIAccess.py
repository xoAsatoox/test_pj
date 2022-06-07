import json
import requests


class APIAccess:
    def __init__(self, config):
        self._auth_server = config['Server']['Auth']
        self.uri_api = None
        self.defaultUser = config['Auth']['User']
        self.defaultPass = config['Auth']['Pass']
        self.timeout = (config['Connection']['Timeout']['Connect'], config['Connection']['Timeout']['Read'])
        self.token = config['Auth']['Token']
        self.commonHeaders = config['Connection']['Headers']
        self.commonHeaders['Authorization'] = config['Auth']['Token']

    def readyAccess(self, isGetToken: bool = True):
        if isGetToken:
            self.token = self.getToken()
            self.commonHeaders['Authorization'] = self.token

    def setURI(self, uri: str):
        self.uri_api = uri

    def getToken(self, user=None, password=None):
        if user is None:
            user = self.defaultUser
        if password is None:
            password = self.defaultPass
        print('Authorization start')
        try:
            req_path = "/GetCognitoToken"
            req_url = self._auth_server
            req_body = {"user": user, "password": password}
            res = requests.post(
                req_url + req_path, data=json.dumps(req_body), timeout=self.timeout
            )
            if 200 == res.status_code:
                token = res.text
            else:
                token = None
        except BaseException:
            token = None
        print('Authorization end')
        return token

    # APIアクセス用関数(GET)
    def get(self, path='', params={}, addheaders=None):

        if self.token is None:
            raise Exception("No token")

        uri = self.uri_api
        if path != '':
            uri = '{}{}'.format(uri, path)

        print(uri)

        headers = self.commonHeaders.copy()
        if addheaders is not None:
            headers.update(addheaders)

        res = requests.get(uri, headers=headers, params=params, timeout=self.timeout)
        if 200 != res.status_code:
            return None

        try:
            body = res.json()
        except Exception:
            return None
        else:
            return body

    # APIアクセス用関数(POST)
    def post(self, path, params, addheaders=None):
        if self.token is None:
            raise Exception("No token")

        uri = self.uri_api
        if path != '':
            uri = '{}{}'.format(uri, path)

        print(uri)

        headers = self.commonHeaders.copy()
        if addheaders is not None:
            headers.update(addheaders)

        res = requests.post(uri, headers=headers, params=params, timeout=self.timeout)
        if 200 != res.status_code:
            return None

        try:
            body = res.json()
        except Exception:
            return None
        else:
            return body
