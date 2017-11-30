import requests


class Publisher(object):
    def __init__(self, server_address = 'http://192.168.30.125:8080', \
                        api_path = '/api/hackathon/device/meas/hackathon_1511958011861',\
                        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ImhhY2thdGhvbl8xNTExOTU4MDExODYxIGhhY2thdGhvbiI.WaWzBFAxQn5EztPoOTYoj8Wdq0S_8u8eCBQLwMe_qW8'):
        self.server_address = server_address #'http://192.168.30.122:8080'
        self.api_path = api_path #'/api/hackathon/device/meas/hackathon_1511958011861'
        self.token = token #'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ImhhY2thdGhvbl8xNTExOTU4MDExODYxIGhhY2thdGhvbiI.WaWzBFAxQn5EztPoOTYoj8Wdq0S_8u8eCBQLwMe_qW8'
        
    def publishData(self, payload):
        url = self.server_address + self.api_path
        headers = {
            'content-type': 'application/json',
            'x-access-token': self.token
        }
        r = requests.post(url, json=payload, headers=headers)
        return r.json()


        #print publishData({'temp': 36, 'threshold': 37})

