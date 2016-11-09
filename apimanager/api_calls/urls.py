from django.conf.urls import url

from .views import GroupedView, ListView

urlpatterns = [
    url(r'^grouped$', GroupedView.as_view(), name='api-calls-grouped'),
    url(r'^list$', ListView.as_view(), name='api-calls-list'),
]
