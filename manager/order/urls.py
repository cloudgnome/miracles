from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^ttn',ttn),
    url(r'^tracking',tracking),
    url(r'^mass_sms/(?P<type>[a-zA-Z]+)',mass_sms),
    url(r'^track/(?P<id>[0-9]+)',track),
    url(r'^sms/(?P<id>[0-9]+)/(?P<type>[a-zA-Z]+)',sms),
    url(r'^search/(?P<query>[a-zA-Z0-9\-\/\_а-яА-Я\[\]\.\, ]+)',CartView.as_view()),
    url(r'^add/(?P<product_id>[0-9]+)/(?P<order_id>[0-9]+)',add),
    url(r'^remove/(?P<id>[0-9]+)',remove)
]