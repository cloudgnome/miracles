from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CartView.as_view(), name = 'cart'),
    url(r'^clear/', views.ClearView.as_view(), name = 'clear'),
    url(r'^remove/(?P<id>[0-9]+)/', views.RemoveView.as_view(), name = 'remove'),
    url(r'^checkout/', views.checkout, name="checkout")
]