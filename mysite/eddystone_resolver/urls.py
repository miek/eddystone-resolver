from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^beacon/$', views.beacons, name='beacons'),
    url(r'^beacon/(?P<beacon_name>[A-Za-z0-9 _-]+)/$', views.beacon, name='beacon'),
    url(r'^eid/(?P<beacon_eid>[A-Fa-f0-9]{16})/$', views.resolve_eid, name='resolve_eid'),
]
