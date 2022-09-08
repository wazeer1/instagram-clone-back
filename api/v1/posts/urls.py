from django.urls import path, re_path


from . import views

app_name = "api_v1_posts"


urlpatterns = [
    re_path(r'^create/post/$', views.create_post),
    re_path(r'^view/posts/$', views.view_posts),
    re_path(r'^like/post/(?P<pk>.*)/$', views.like_post),
    re_path(r'^comment/post/(?P<pk>.*)/$', views.comment_post),
    re_path(r'^view/comment/(?P<pk>.*)/$', views.comment_view),
]