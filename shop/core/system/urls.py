# -*- coding=utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from catalog import views as catalog
from shop.views.sitemaps import sitemap
from shop.views import RobotsView,ConfirmView
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^redactor/', include('redactor.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/image/favicon.png')),
    url(r'^sitemap\.xml$', sitemap, name='sitemapxml'),
    url(r'^robots\.txt$', RobotsView.as_view(), name='robots'),
    url(r'^\.well-known/pki-validation/(?P<name>\w+\.txt)$', ConfirmView.as_view()),
    url(r'^1c/',include('catalog.urls')),
    url(r'^(?P<lang>(ua))/', include('shop.urls')),
    url(r'^', include('shop.urls')),
]

from shop.views import error404,error500

handler404 = error404
handler500 = error500

urlpatterns.append(url(r'^(?P<lang>(ua))/(?P<slug>.*)', catalog.resolve ,name='catalog'))
urlpatterns.append(url(r'^(?P<slug>.*)', catalog.resolve ,name='catalog'))


urlpatterns.append(url(r'^$', include('shop.urls')))