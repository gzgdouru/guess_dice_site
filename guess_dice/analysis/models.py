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
    custom_prediction = models.CharField(max_length=16, verbose_name="自定义预测", default="")
    three_balance = models.DecimalField(max_digits=13, decimal_places=2, default=0.00, verbose_name="三期余额")
    five_balance = models.DecimalField(max_digits=13, decimal_places=2, default=0.00, verbose_name="五期余额")
    seven_balance = models.DecimalField(max_digits=13, decimal_places=2, default=0.00, verbose_name="七期余额")
    nine_balance = models.DecimalField(max_digits=13, decimal_places=2, default=0.00, verbose_name="九期余额")
    eleven_balance = models.DecimalField(max_digits=13, decimal_places=2, default=0.00, verbose_name="十一期余额")
    custom_balance = models.DecimalField(max_digits=13, decimal_places=2, default=0.00, verbose_name="自定义余额")
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    class Meta:
        db_table = "tb_guess_dice"

    def __str__(self):
        return self.period


class ClientIp(models.Model):
    ip = models.CharField(max_length=64, verbose_name="客户端ip")
    url = models.CharField(max_length=255, verbose_name="访问链接", default="")
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    class Meta:
        db_table = "tb_client_ip"

    def __str__(self):
        return self.ip
