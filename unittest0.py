"""
Unittest

大部分接口涉及前端交互，且需要微信小程序提供的code或前端的storage中存储的加密open_id
不方便进行自动化测试，在功能测试部分已经进行了充分的等价类划分和测试
"""


import requests
import json
import unittest

url = "https://c02.whiteffire.cn:8000/"
class BackendTest(unittest.TestCase):
    
    def test_static(self):
        resp = requests.get(url+"log/static/")
        self.assertTrue(resp.status_code==200)
        resp = requests.get(url+"dorm/static/")
        self.assertTrue(resp.status_code==200)
        resp = requests.get(url+"guest/static/")
        self.assertTrue(resp.status_code==200)
        resp = requests.get(url+"guard/static/")
        self.assertTrue(resp.status_code==200)
    def test_backstage(self):
        resp = requests.get(url+"guard/backstage/")
        self.assertTrue(resp.status_code==200)
    def test_blacklist(self):
        # 正确输入
        data = [
            {"open_id":"o-dQg4188ZEmjJSJQPbBa52b7ll0"},
            {"open_id":"o-dQg4zF1XZIZTxQS9phiwlOqYwQ"}
        ]
        resp = requests.post(url+'guest/to_black/',data=json.dumps(data),headers={'content-type': 'application/json'})
        self.assertTrue(resp.status_code==200)
        # 错误输入
        data = [
            {"open_id":"o-dQ"},
        ]
        resp = requests.post(url+'guest/to_black/',data=json.dumps(data),headers={'content-type': 'application/json'})
        self.assertTrue(resp.status_code==500)
    def test_whitelist(self):
        # 正确输入
        data = [
            {"open_id":"o-dQg4188ZEmjJSJQPbBa52b7ll0"},
            {"open_id":"o-dQg4zF1XZIZTxQS9phiwlOqYwQ"}
        ]
        resp = requests.post(url+'guest/to_white/',data=json.dumps(data),headers={'content-type': 'application/json'})
        self.assertTrue(resp.status_code==200)

        #错误输入
        data = [
            {"open_id":"o-dQ"},
        ]
        resp = requests.post(url+'guest/to_white/',data=json.dumps(data),headers={'content-type': 'application/json'})
        self.assertTrue(resp.status_code==500)
    def test_admin(self):
        # 正确密码
        data = {"password":"123456"}
        resp = requests.post(url+'guard/admin_login/',data=data)
        self.assertTrue(resp.status_code==200)
        data = {"password":"12346"}

        #错误密码
        resp = requests.post(url+'guard/admin_login/',data=data)
        self.assertTrue(resp.status_code==203)

        resp = requests.get(url+"guard/admin_userinfo/")
        self.assertTrue(resp.status_code==200)
if __name__ == '__main__':
    unittest.main()