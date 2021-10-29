from django.conf.urls import url
from user.views import *
from user.decorators import login_required

urlpatterns = [
    url(r'^signup/$', SignupView.as_view(),name='signup'),
    url(r'^profile/$', login_required(ProfileView.as_view()), name="profile"),
    url(r'^order/(?P<id>[0-9]+)$', login_required(OrderView.as_view()), name="order"),
    url(r'^signin/$', SigninView.as_view(), name="login"),
    url(r'^signout/$', signout, name="signout"),
    url(r'^forget-password/$',forget_password,name='forget-pass'),
    url(r'^change-password$',ChangePasswordView.as_view(),name='change-password'),
    url(r'^pay/callback$',pay_callback),
    url(r'^favorite/',favorite),
    url(r'^compare/',compare)
]