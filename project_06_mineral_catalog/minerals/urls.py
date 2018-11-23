from django.conf.urls import url


from . import views
from django.conf.urls.i18n import urlpatterns

urlpatterns = [
    url(r'^$', views.mineral_list, name='list'),
    url(r'(?P<pk>\d+)/$', views.mineral_detail, name='detail'),
    ]
    