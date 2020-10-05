from django.urls import path
from . import views

from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),


    url(r'^aboutus', views.aboutus, name='aboutus'),
    url(r'^video$', views.testvideo, name='video'),
    url(r'^video$', views.testvideo, name='video'),
    url(r'^video/(?P<cid>.*)/(?P<name>.*)$', views.viewvideo, name='video'),
    url(r'^videocid', views.video_cid, name='videocid'),

]
