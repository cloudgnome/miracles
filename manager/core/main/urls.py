from django.conf.urls import url
from .views import *
from user.views import signout
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'api/Item', ItemViewSet)
router.register(r'api/Product', ProductViewSet)

urlpatterns = [
    url(r'^autocomplete/(?P<Model>[a-zA-Z]+)/(?P<value>.*)$',autocomplete),
    url(r'^delivery/city/(?P<type>[0-9])/(?P<value>.*)$',city),
    url(r'^delivery/departament/(?P<type>[0-9])/(?P<city_id>[0-9]+)/$',departaments),
    url(r'^delivery/departament/(?P<type>[0-9])/(?P<city_id>[0-9]+)/(?P<value>.*)$',departaments),
    url(r'^prices$', PricesView.as_view(), name='prices'),
    url(r'^stock$', StockView.as_view(), name='stock'),
    url(r'^search/(?P<Model>[a-zA-Z]+)$',search),
    url(r'^gallery/(?P<Model>[a-zA-Z]+)/(?P<id>[0-9]+)/ordering$',ordering),
    url(r'^(?P<Model>[A-Z][a-z]+)$',List.as_view()),
    url(r'^(?P<Model>[A-Z][a-z]+)/$',AddView.as_view()),
    url(r'^(?P<Model>[A-Z][a-z]+)/(?P<id>[0-9]+)$',EditView.as_view()),
    url(r'^change_database',change_database),
    url(r'^task$',task),
    url(r'^drop_cache',drop_cache),
    url(r'^action/(?P<product_id>[0-9]+)/availability$',availability),
    url(r'^action/(?P<type>[a-z]+)$',action),

    url(r'^product/(?P<product_id>[0-9]+)/info$',product_export),
    url(r'^product/(?P<product_id>[0-9]+)/update$',product_update_export),

    url(r'^signout',signout),
    url(r'^$',index)
]

urlpatterns += router.urls