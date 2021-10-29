from django.conf.urls import url
from blog.views import ArticleView
from django.contrib.auth.decorators import login_required

from catalog.views import *

urlpatterns = [
    url(r'^quick_view/(?P<id>[0-9]+)$',Quick_View.as_view(),name='quick'),
    url(r'^search/',search,name="search"),
    url(r'^pricelist/$',PriceList.as_view(),name="pricelist"),
    url(r'^brands/$',BrandsView.as_view(),name="brands"),
    url(r'^category/(?P<id>[0-9]+)',CategoryView.as_view(),name="category"),
    url(r'^product/(?P<id>[0-9]+)',ProductView,name="product"),
    url(r'^article/(?P<id>[0-9]+)',ArticleView.as_view(),name="article"),
    url(r'^feedback',FeedbackView.as_view(),name="feedback"),
    url(r'^rating/(?P<id>[0-9]+)/(?P<value>[1-5])',rating)
]