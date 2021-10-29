from django.conf.urls import include, url
from catalog import views as catalog
from blog import views as blog
from shop.views import maintenance,HomeView,GuestbookView,categories

urlpatterns = [
    url(r'^user/', include('user.urls')),
    url(r'^(?P<lang>(ua))/user/', include('user.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^(?P<lang>(ua))/cart/', include('cart.urls')),
    url(r'^checkout/', include('checkout.urls')),
    url(r'^(?P<lang>(ua))/checkout/', include('checkout.urls')),
    url(r'^catalog/',include('catalog.urls')),
    url(r'^(?P<lang>(ua))/catalog/',include('catalog.urls')),
    # url(r'^filter', catalog.filter, name='filter'),
    url(r'^maintenance\.html',maintenance),
    url(r'^search', catalog.search, name='search'),
    url(r'^(?P<lang>(ua))/search', catalog.search, name='search'),
    url(r'^leave_review', GuestbookView.as_view()),
    url(r'^(?P<lang>(ua))/categories',categories),
    url(r'^categories',categories)
]