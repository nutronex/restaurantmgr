from django.conf.urls import url
from .views import index,day_view,api_day_view

urlpatterns =[
        url('^day/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d*)$',day_view),
        url('^$',index),
        ]
