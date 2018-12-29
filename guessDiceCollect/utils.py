import requests
import json
from datetime import datetime


def send_sms(mobile, period, code, open_time):
    url = r'https://api.mysubmail.com/message/xsend'
    params = {
        "period": period,
        "code": code,
        "time": open_time,
    }

    data = {
        "appid": "27038",
        "to": mobile,
        "project": "qq7qZ",
        "vars": json.dumps(params),
        "signature": "c7ed55eb026edf67c87183a28948872a",
    }

    session = requests.session()
    response = session.post(url, data=data)
    res = json.loads(response.text)
    if res.get("status") != "error":
        print(f"发送短信给用户[{mobile}]成功.")
    else:
        err = res.get("msg")
        print(f"发送短信给用户[{mobile}]失败, 原因:{err}!")

if __name__ == "__main__":
    mobile = "13590009594"
    period = "测试葛"
    code = "17"
    open_time = datetime.now().strftime("%Y-%m-%d %H%M%S")
    send_sms(mobile, period, code, open_time)
