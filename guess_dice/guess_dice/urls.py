"""guess_dice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from analysis.views import IndexView, PeriodStatsView, ProbabilityStatsView, PredictionView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^nums/(?P<period_count>\d+)/$', PeriodStatsView.as_view(), name="nums_stats"),
    url(r'^probability/(?P<prediction_num>(0|3|5|7|9|11))/$', ProbabilityStatsView.as_view(), name="probability_stats"),
    url(r'^prediction/$', PredictionView.as_view(), name="prediction"),
]
