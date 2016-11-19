from django.conf.urls import url

from .views import IndexView, DetailView, EnableView, DisableView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='consumers-index'),
    url(r'^(?P<consumer_id>[0-9]+)$', DetailView.as_view(), name='consumers-detail'),
    url(r'^(?P<consumer_id>[0-9]+)/enable$', EnableView.as_view(), name='consumers-enable'),
    url(r'^(?P<consumer_id>[0-9]+)/disable$', DisableView.as_view(), name='consumers-disable'),
]
