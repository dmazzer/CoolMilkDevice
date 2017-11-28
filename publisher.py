import requests


class Publisher(object):
    def __init__(self, server_address, api_path, token)
    {
        self.server_address = server_address #'http://192.168.99.100:8080'
        self.api_path = api_path #'/api/inatel/device/meas/inatel_1511882730181'
        self.token = token #'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ImluYXRlbF8xNTExODgyNzMwMTgxIGluYXRlbCI.TYtXGAgTZTwQRV0hBpke8381z8-eYyvHSAaeyATI2H8'
    }
        
    def publishData(payload):
        url = self.server_address + self.api_path
        headers = {
            'content-type': 'application/json',
            'x-access-token': self.token
        }
        r = requests.post(url, json=payload, headers=headers)
        return r.json()


    print publishData({'temp': 36, 'threshold': 37})

