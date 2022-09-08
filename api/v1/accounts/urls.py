from django.urls import path, re_path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

app_name = "api_v1_accounts"


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^register/$', views.register),
    re_path(r'^login/$', views.login),
    re_path(r'^setbirthday/$', views.setbirthday),
    re_path(r'^minimals/$', views.minimals),
    re_path(r'^users/view/$', views.users_view),
    re_path(r'^send/request/(?P<pk>.*)/$', views.send_request),
    re_path(r'^requests/$', views.request_list),
]