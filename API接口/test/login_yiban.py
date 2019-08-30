# coding=utf8

from flask import Flask, request
import requests

app = Flask(__name__)

class yiban:
    def __init__(self):
        self.app_code = ""
        self.access_token = ""

@app.route("/backurl")
def login_yiban():
    # 获取code
    code = str(request.args.get("code"))
    yiban_user.app_code = code
    # 获取access_token
    url = "https://oauth.yiban.cn/token/info?code=%(CODE)s&client_id=%(APPID)s&" \
          "client_secret=%(APPSECRET)s&redirect_uri=%(CALLBACK)s"%{"CODE": yiban_user.app_code, "APPID": app_id,
                                                                  "APPSECRET": app_secret, "CALLBACK": back_url}
    response = requests.request("GET", url)
    yiban_user.access_token = response.json()["access_token"]
    get_user_info(yiban_user)
    return "hello", 200

def get_user_info(yiban_user):
    payload = {"access_token": yiban_user.access_token}
    url = "https://openapi.yiban.cn/user/me"
    response = requests.request("GET", url, params=payload)
    print(response.text)
    print(response.json()["info"]["yb_username"])

if __name__ == "__main__":
    yiban_user = yiban()
    app_id = "c751a57fd14a86f4"
    app_secret = "923460388580b30507e5deaacd08f39e"
    back_url = "http://120.79.142.251:5000/backurl"
    app.run(host="0.0.0.0", port=5000, debug=True)