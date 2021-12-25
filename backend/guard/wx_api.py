from rest_framework.response import Response
import requests
from hashlib import sha256
import hmac

def code2Session(appId, appSecret, code):
    payload = { 
            "appid": appId,
            "secret": appSecret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
    r = requests.get('https://api.weixin.qq.com/sns/jscode2session',params=payload)
    packet = eval(r.text)
    openid=""
    session_key=""
    unionid="" # discard in iter stage 1
    openid = packet.get("openid")
    session_key = packet.get("session_key")
    return {"open_id":openid,"session_key":session_key}
        
def getAccessToken(appId, appSecret):
    payload = {
        "appid": appId,
        "secret": appSecret,
        "grant_type": "client_credential",
    }
    r = requests.get("https://api.weixin.qq.com/cgi-bin/token",params=payload)
    packet = eval(r.text)
    return packet.get("access_token")

# abort
def getUserEncryptKey(access_token,openid,session_key):
    raw=""
    signature = hmac.new(session_key.encode(),raw.encode(),digestmod=sha256).hexdigest()
    data = {
        "access_token": access_token,
        "openid": openid,
        "signature": signature,
        "sig_method": "hmac_sha256",
    }
    r = requests.post("https://api.weixin.qq.com/wxa/business/getuserencryptkey",data=data)
    packet = eval(r.text)
    key_info_list=packet.get("key_info_list")
    return key_info_list[0]