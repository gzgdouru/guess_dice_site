from datetime import datetime
from collections import Counter
from operator import itemgetter

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Dice, ClientIp
from .utils import result_prediction, DiceInfo, value_convert, PREDICTION_DICT, get_day_stats, custom_prediction


# Create your views here.

class IndexView(View):
    def get(self, request):
        num_list = []
        history_records = []
        total_counter = {}
        period_count = 0

        for dice in Dice.objects.all().order_by("-period"):
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
            "days_stats": dict(days_stats),
        })


class BaseStatsView(View):
    def get(self, request):
        period = None
        total_counter = {}
        period_count = 0
        num_list = []

        for dice in Dice.objects.all().order_by("-period"):
            period_count += 1
            if not period:
                period = int(dice.period)
            total_counter[dice.total] = total_counter.get(dice.total, 0) + 1
            num_list.extend([dice.num_1, dice.num_2, dice.num_3])
        total_counter = dict(sorted(total_counter.items(), key=itemgetter(1), reverse=True))
        numsCounter = Counter(num_list)
        nums = numsCounter.most_common()
        del num_list

        days_stats = get_day_stats()

        return render(request, "base-stats.html", context={
            "period": period,
            "period_count": period_count,
            "days_stats": days_stats,
            "nums": nums,
            "total_counter": total_counter,
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
        predictions.append(("自定义", custom_prediction(dices[:3])))
        predictions.append(("三期统计", result_prediction(dices[:3])))
        predictions.append(("五期统计", result_prediction(dices[:5])))
        predictions.append(("七期统计", result_prediction(dices[:7])))
        predictions.append(("九期统计", result_prediction(dices[:9])))
        predictions.append(("十一期统计", result_prediction(dices[:11])))

        return render(request, "prediction.html", context={
            "period": period,
            "predictions": predictions,
        })


class VisitShowView(View):
    def get(self, request):
        all_visitors = ClientIp.objects.all().order_by("-add_time")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_visitors, 50, request=request)
        visitors = p.page(page)
        return render(request, "visitors-show.html", context={
            "visitors" : visitors,
        })