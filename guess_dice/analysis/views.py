from datetime import datetime

from django.shortcuts import render
from django.views.generic import View
from collections import Counter
from operator import itemgetter

from .models import Dice
from .utils import result_prediction, DiceInfo, value_convert, PREDICTION_DICT, get_day_stats


# Create your views here.

class IndexView(View):
    def get(self, request):
        num_list = []
        history_records = []
        total_counter = {}
        period_count = 0

        for dice in Dice.objects.all().order_by("-id"):
            period_count += 1
            total_counter[dice.total] = total_counter.get(dice.total, 0) + 1

            if len(history_records) < 25:
                history_records.append(dice)

            num_list.extend([dice.num_1, dice.num_2, dice.num_3])
        total_counter = dict(sorted(total_counter.items(), key=itemgetter(1), reverse=True))

        period = int(history_records[0].period)
        numsCounter = Counter(num_list)
        nums = numsCounter.most_common()
        del num_list

        prediction = result_prediction(history_records[:3])
        days_stats = get_day_stats()

        return render(request, "index.html", context={
            "prediction": prediction,
            "nums": nums,
            "period": period,
            "period_count": period_count,
            "history_records": history_records,
            "total_counter": total_counter,
            "days_stats" : dict(days_stats),
        })


class PeriodStatsView(View):
    def get(self, request, period_count):
        num_list = []
        period_count = int(period_count)
        dices = Dice.objects.all().order_by("-period")[:10]

        [num_list.extend([dice.num_1, dice.num_2, dice.num_3]) for dice in dices[:period_count]]

        numsCounter = Counter(num_list)
        numsStats = numsCounter.most_common()
        numsStats = sorted(numsStats, key=itemgetter(0), reverse=True)
        del num_list

        first_period = dices[period_count - 1].period
        last_period = dices[0].period

        return render(request, "nums-stats.html", context={
            "dices": dices,
            "numsStats": numsStats,
            "first_period": first_period,
            "last_period": last_period,
        })


class ProbabilityStatsView(View):
    def get(self, request, prediction_num):
        period_count = int(request.GET.get("period_count", 30))
        dices = Dice.objects.all().order_by("-period")[:period_count]
        right_count = 0
        for dice in dices:
            dice.prediction = getattr(dice, PREDICTION_DICT.get(prediction_num))
            if value_convert(dice.total) == dice.prediction:
                right_count += 1
        probability = (right_count / period_count) * 100

        first_period = dices[period_count - 1].period
        last_period = dices[0].period

        return render(request, "probability-stats.html", context={
            "dices": dices,
            "probability": probability,
            "first_period": first_period,
            "last_period": last_period,
            "prediction_num": prediction_num,
            "period_count": period_count,
        })


class PredictionView(View):
    def get(self, request):
        dices = Dice.objects.all().order_by("-period")[:11]
        period = int(dices[0].period) + 1
        predictions = []
        predictions.append((3, result_prediction(dices[:3])))
        predictions.append((5, result_prediction(dices[:5])))
        predictions.append((7, result_prediction(dices[:7])))
        predictions.append((9, result_prediction(dices[:9])))
        predictions.append((11, result_prediction(dices[:11])))

        return render(request, "prediction.html", context={
            "period" : period,
            "predictions": predictions,
        })
