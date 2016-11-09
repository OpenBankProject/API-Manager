from django.conf.urls import url

from .views import IndexView, EnableView, DisableView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='consumers-index'),
    url(r'^enable/(?P<consumer_id>[0-9]+)$', EnableView.as_view(), name='consumers-enable'),
    url(r'^disable/(?P<consumer_id>[0-9]+)$', DisableView.as_view(), name='consumers-disable'),
]
