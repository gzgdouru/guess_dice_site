import random
from datetime import datetime
from collections import Counter, namedtuple
from operator import itemgetter
from selenium import webdriver
import time
from lxml import etree
import sys
import requests
import json

from fake_useragent import UserAgent

from mysqlV1 import MysqlManager
from log_settings import logger
from guessDiceUtils import result_prediction, custom_prediction, get_money
from utils import send_sms

LK3Info = namedtuple("LK3Info", ["period", "num_1", "num_2", "num_3"])

mysqlConfig = {
    "host": "193.112.150.18",
    "port": 3306,
    "user": "ouru",
    "password": "5201314Ouru...",
    "db": "novel",
    "charset": "utf8",
    "max_overflow": 5,
}
mysqldb = MysqlManager(**mysqlConfig)
ua = UserAgent()
mobile_list = ["13590009594"]

def get_nums(value):
    nums = [int(num) for num in str(value).split(",")]
    return nums


def get_proxy():
    records = mysqldb.select("proxys", conditions="score > 0", order_by="rand()", limit=1)
    for record in records:
        return record.ip, record.port
    return None, None


def get_response(url, headers, try_time=3):
    ip, port = get_proxy()
    try:
        if ip and port:
            logger.info("通过代理[{0}:{1}]访问!".format(ip, port))
            proxy = "http://{0}:{1}".format(ip, port)
            proxies = {"https": proxy}
            response = requests.get(url=url, headers=headers, proxies=proxies, timeout=30)
        else:
            logger.info("找不到代理IP, 通过本机IP访问!")
            response = requests.get(url=url, headers=headers, timeout=10)
    except:
        try_time -= 1
        logger.info("通过代理[{0}:{1}]访问失败, 再尝试{2}次代理访问!".format(ip, port, try_time))
        if try_time <= 0:
            logger.info("代理访问失败, 通过本机ip访问!")
            response = requests.get(url=url, headers=headers, timeout=10)
        else:
            response = get_response(url, headers, try_time)
    return response


def get_records(url, headers):
    records = []
    try:
        response = get_response(url, headers)
        data_type = response.headers["Content-Type"]
        records = []
        if -1 != data_type.find("json"):
            # json格式返回
            records = json.loads(response.text)
        elif -1 != data_type.find("xml"):
            # xml格式返回
            xml_tree = etree.XML(response.text, etree.XMLParser())
            item_nodes = xml_tree.xpath("//item")
            for node in item_nodes:
                record = {}
                record["openCode"] = node.xpath("openCode/text()")[0]
                record["officialOpenTimeEpoch"] = node.xpath("officialOpenTimeEpoch/text()")[0]
                record["uniqueIssueNumber"] = node.xpath("uniqueIssueNumber/text()")[0]
                records.append(record)
        else:
            logger.error("未知的数据格式, 数据格式:{0}, 数据内容:{1}".format(data_type, response.text))
    except Exception as e:
        logger.error("数据解析出错, 错误原因:{1}".format(e))
    return records


def parse_info():
    url = r'https://1064444.cc/api/v1/result/service/mobile/results/hist/HF_LFK3?limit=40'
    headers = {"User-Agent": ua.random}
    today = datetime.now().day

    while True:
        time_start = time.time()
        records = get_records(url, headers)
        try:
            for record in records:
                nums = get_nums(record["openCode"])
                period = record["uniqueIssueNumber"]
                times = record.get("officialOpenTimeEpoch", datetime.now().timestamp())
                open_time = datetime.fromtimestamp(int(times)).strftime("%Y-%m-%d %H:%M:%S")
                if mysqldb.exist("tb_guess_dice", conditions="period='{0}'".format(period)):
                    logger.info("记录[{0}({1}, {2}, {3})]已存在.".format(period, nums[0], nums[1], nums[2]))
                    break  # 最新一期存在的话, 后面缺的就不补了
                else:
                    if datetime.now().day == today:
                        is_same_day = True
                    else:
                        is_same_day = False
                        today = datetime.now().day

                    history_records = list(mysqldb.select("tb_guess_dice", order_by="-period", limit=11))
                    three_prediction = result_prediction(history_records[:3])
                    five_prediction = result_prediction(history_records[:5])
                    seven_prediction = result_prediction(history_records[:7])
                    nine_prediction = result_prediction(history_records[:9])
                    eleven_prediction = result_prediction(history_records[:11])
                    customPrediction = custom_prediction(history_records[:3])

                    total = sum(nums)
                    if total == 17:
                        [send_sms(mobile, period, str(nums), open_time) for mobile in mobile_list]

                    three_balance = get_money(three_prediction, total, history_records[0].three_balance, is_same_day)
                    five_balance = get_money(five_prediction, total, history_records[0].five_balance, is_same_day)
                    seven_balance = get_money(seven_prediction, total, history_records[0].seven_balance, is_same_day)
                    nine_balance = get_money(nine_prediction, total, history_records[0].nine_balance, is_same_day)
                    eleven_balance = get_money(eleven_prediction, total, history_records[0].eleven_balance, is_same_day)
                    custom_balance = get_money(customPrediction, total, history_records[0].custom_balance, is_same_day)

                    mysqldb.insert("tb_guess_dice", period=period, num_1=nums[0], num_2=nums[1], num_3=nums[2],
                                   add_time=datetime.now(), total=total, three_prediction=three_prediction,
                                   five_prediction=five_prediction, seven_prediction=seven_prediction,
                                   nine_prediction=nine_prediction, eleven_prediction=eleven_prediction,
                                   custom_prediction=customPrediction, three_balance=three_balance,
                                   five_balance=five_balance, seven_balance=seven_balance, nine_balance=nine_balance,
                                   eleven_balance=eleven_balance, custom_balance=custom_balance)
                    logger.info("记录[{0}({1}, {2}, {3})]保存成功.".format(period, nums[0], nums[1], nums[2]))
        except Exception as e:
            logger.error("提取信息出错, 错误原因:{0}!".format(e))
        time_end = time.time()
        logger.info("提取信息完成, 耗时:{0}".format(time_end - time_start))

        sleep_time = random.randint(20, 30)
        logger.info("休眠{0}秒!".format(sleep_time))
        time.sleep(sleep_time)


if __name__ == "__main__":
    parse_info()