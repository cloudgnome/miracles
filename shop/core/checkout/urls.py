from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^order/$', views.OrderView.as_view(), name ='order'),
    url(r'^city/(?P<type>[0-9])/(?P<value>.*)$', views.CityView.as_view(), name='city'),
    url(r'^departament/(?P<type>[0-9])/(?P<value>.*)/(?P<city>[0-9]+)$', views.DepartamentView.as_view(), name='departament'),
    url(r'^departament/(?P<type>[0-9])/(?P<city>[0-9]+)$', views.DepartamentView.as_view(), name='departament'),
    url(r'^quick_order/(?P<id>[0-9]+)/(?P<qty>[0-9]+)$', views.CallbackView.as_view(), name='quick_order'),
    url(r'^remove/(?P<id>[0-9]+)/', views.remove, name='remove'),
    url(r'^callback/$',views.CallbackView.as_view(),name='callback'),
    url(r'^callback/(?P<id>[0-9]+)$',views.CallbackView.as_view(),name='callback'),
    url(r'^', views.CheckoutView.as_view(), name ='checkout'),
]