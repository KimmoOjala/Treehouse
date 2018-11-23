from django.conf.urls import url


from . import views
from django.conf.urls.i18n import urlpatterns

urlpatterns = [
    url(r'^$', views.course_list),
    url(r'(?P<course_pk>\d+)/(?P<step_pk>\d+)', views.step_detail),
    url(r'(?P<pk>\d+)/$', views.course_detail), 
    ]
    
