import hashlib
import hmac
import time
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TuyaAPI:
    @staticmethod
    def get_sign(client_id, secret, method, url, token=None):
        t = str(int(time.time() * 1000))
        body_hash = hashlib.sha256(b"").hexdigest()
        string_to_sign = f"{method}\n{body_hash}\n\n{url}"
        message = (client_id or "") + (token if token else "") + t + string_to_sign
        sign = hmac.new((secret or "").encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest().upper()
        return sign, t

    @staticmethod
    def get_token(region, client_id, secret):
        endpoint = f"https://openapi.tuya{region}.com"
        path = "/v1.0/token?grant_type=1"
        sign, t = TuyaAPI.get_sign(client_id, secret, "GET", path)
        headers = {"client_id": client_id, "sign": sign, "t": t, "sign_method": "HMAC-SHA256"}
        r = requests.get(endpoint + path, headers=headers, timeout=2).json()
        return r

    @staticmethod
    def get_status(region, client_id, secret, device_id, token):
        endpoint = f"https://openapi.tuya{region}.com"
        path = f"/v1.0/devices/{device_id}/status"
        sign, t = TuyaAPI.get_sign(client_id, secret, "GET", path, token=token)
        headers = {"client_id": client_id, "sign": sign, "t": t, "access_token": token, "sign_method": "HMAC-SHA256"}
        r = requests.get(endpoint + path, headers=headers, timeout=2).json()
        return r