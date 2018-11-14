from django.db import models

# Create your models here.


class Dice(models.Model):
    period = models.CharField(max_length=32, verbose_name="周期", unique=True)
    num_1 = models.PositiveIntegerField(verbose_name="数字1")
    num_2 = models.PositiveIntegerField(verbose_name="数字2")
    num_3 = models.PositiveIntegerField(verbose_name="数字3")
    total = models.PositiveIntegerField(verbose_name="和值", default=0)
    three_prediction = models.CharField(max_length=16, verbose_name="三期预期", default="")
    five_prediction = models.CharField(max_length=16, verbose_name="五期预测", default="")
    seven_prediction = models.CharField(max_length=16, verbose_name="七期预测", default="")
    nine_prediction = models.CharField(max_length=16, verbose_name="九期预测", default="")
    eleven_prediction = models.CharField(max_length=16, verbose_name="十一期预测", default="")
    custom_prediction = models.CharField(max_length=16, verbose_name="自定义", default="")
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    class Meta:
        db_table = "tb_guess_dice"

    def __str__(self):
        return self.period