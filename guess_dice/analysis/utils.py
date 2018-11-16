from collections import Counter, namedtuple, defaultdict
from operator import itemgetter

from django.db import connection

DiceInfo = namedtuple("DiceInfo", ["period", "num_1", "num_2", "num_3", "total", "prediction"])

PREDICTION_DICT = {
    "0": "custom_prediction",
    "3": "three_prediction",
    "5": "five_prediction",
    "7": "seven_prediction",
    "9": "nine_prediction",
    "11": "eleven_prediction",
}


def result_prediction(history_records):
    if not history_records:
        return "未知"

    # 发疯状态, 连续开, 3期及以上
    if is_period_same(history_records[:3], "大"):
        return "大"
    elif is_period_same(history_records[:3], "小"):
        return "小"

    # 按大小个数分析
    maxCount, minCount = get_maxmin_count(history_records)
    return "小" if maxCount > minCount else "大"


def get_maxmin_count(history_records):
    num_list = []
    [num_list.extend([dice.num_1, dice.num_2, dice.num_3]) for dice in history_records]
    numsCounter = Counter(num_list)
    nums = numsCounter.most_common()

    minCount = sum(num[1] for num in nums if num[0] <= 3)
    maxCount = sum(num[1] for num in nums if num[0] > 3)

    return maxCount, minCount


def is_period_same(history_records, value="大"):
    for record in history_records:
        if value != value_convert(record.total):
            return False
    return True


def value_convert(totalCount):
    return "大" if totalCount > 10 else "小"


def get_day_stats():
    data = defaultdict(list)
    cursor = connection.cursor()
    sql = '''
        SELECT DATE_FORMAT(add_time,'%Y%m%d') days,COUNT(id) COUNT FROM tb_guess_dice
          WHERE total <= 10 
          GROUP BY days
        UNION
          SELECT DATE_FORMAT(add_time,'%Y%m%d') days,COUNT(id) COUNT FROM tb_guess_dice
          WHERE total > 10 
          GROUP BY days
    '''
    cursor.execute(sql)
    [data[row[0]].append(row[1]) for row in cursor.fetchall()]
    return dict(sorted(data.items(), key=itemgetter(0), reverse=True))


def get_all_date():
    cursor = connection.cursor()
    sql = "SELECT DISTINCT DATE_FORMAT(add_time, '%Y%m%d') FROM tb_guess_dice"
    cursor.execute(sql)
    date_list = [row[0] for row in cursor.fetchall()]
    return reversed(date_list)


def get_balance_stats_records():
    balance_reocrds = []
    cursor = connection.cursor()
    for d in get_all_date():
        sql = '''
            select {0}, three_balance, five_balance, seven_balance, nine_balance, eleven_balance, custom_balance from tb_guess_dice
            where DATE_FORMAT(add_time, '%Y%m%d') = {0}
            order by period desc limit 1
        '''.format(d)
        cursor.execute(sql)
        reocrd = list(cursor.fetchone())

        sql = '''
            select max(three_balance), min(three_balance), max(five_balance), min(five_balance),
                max(seven_balance), min(seven_balance), max(nine_balance), min(nine_balance),
                max(eleven_balance), min(eleven_balance), max(custom_balance), min(custom_balance)
            from tb_guess_dice
            where DATE_FORMAT(add_time, '%Y%m%d') = {0}
        '''.format(d)
        cursor.execute(sql)
        reocrd.extend(cursor.fetchone())

        balance_reocrds.append(reocrd)
    return balance_reocrds


def custom_prediction(records):
    # 连续三期相同
    if is_period_same(records[:3], "大"):
        return "大"
    elif is_period_same(records[:3], "小"):
        return "小"

    # 连续两期相同
    if is_period_same(records[:2], "大"):
        return "小"
    elif is_period_same(records[:2], "小"):
        return "大"

    # 都不相同
    return value_convert(records[0].total)
