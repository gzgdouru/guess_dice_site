from collections import Counter, namedtuple
from decimal import Decimal

DiceInfo = namedtuple("DiceInfo", ["period", "num_1", "num_2", "num_3", "total", "prediction"])


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
        if value != get_value_convert(record.total):
            return False
    return True


def get_value_convert(totalCount):
    return "大" if totalCount > 10 else "小"


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
    return get_value_convert(records[0].total)


def get_money(prediction, total, balance, is_same_day):
    balance = balance if is_same_day else 0
    if get_value_convert(total) == prediction:
        balance = balance - 2 + (2*Decimal("1.96"))
    else:
        balance -= 2
    return balance
