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


def send_email(email, mobile, code, open_time):
    url = r'https://api.mysubmail.com/mail/xsend'
    params = {
        "period": period,
        "code": code,
        "time": open_time,
    }

    data = {
        "appid": "13955",
        "to": email,
        "subject": "106号码提醒",
        "project": "6q0KG2",
        "vars": json.dumps(params),
        "signature": "2d21d55a5bdc018fbf7123544264dd9b",
    }
    response = requests.post(url, data=data)
    res = json.loads(response.text)
    if res.get("status") != "error":
        print(f"发送邮件给用户[{email}]成功.")
    else:
        err = res.get("msg")
        print(f"发送邮件给用户[{email}]失败, 原因:{err}!")


if __name__ == "__main__":
    email = "18719091650@163.com"
    period = "101"
    code = "17"
    open_time = datetime.now().strftime("%Y-%m-%d %H%M%S")
    send_email(email, period, code, open_time)
