from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^\.well-known/pki-validation/(?P<name>\w+\.txt)$', SignUpView.as_view()),
    url(r'^signup$',SignUpView.as_view()),
    url(r'^category/(?P<id>[0-9]+)$',CategoryView.as_view()),
    url(r'^product/(?P<id>[0-9]+)$',ProductView.as_view()),
    url(r'^city/(?P<type>[-\w]+)$', city),
    url(r'^departament/(?P<type>[-\w]+)/(?P<city>[0-9]+)$', departament),
    url(r'^quick_order$', quick_order),
    url(r'^checkout$',checkout),
    url(r'^search$',search),
    url(r'^orders$',orders),
    url(r'^order/(?P<id>[0-9]+)$',OrderView.as_view()),
    url(r'^departaments$',load_departaments),
    url(r'^user/update',profile),
    url(r'^user/favorites',favorites),
    url(r'^$',HomeView.as_view()),
]