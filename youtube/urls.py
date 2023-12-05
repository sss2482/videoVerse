# from django.conf.urls import  include
from django.contrib import admin
from django.conf import settings
from django.urls import re_path, include, path
from . import views

app_name='youtube'
urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^submit/$',views.submit,name='submit'),
    re_path(r'^signup/$', views.sign_up, name='sign_up'),
    re_path(r'^watch/(?P<video_id>[0-9A-Za-z_-]+)/$', views.watch,name='watch' ),
    re_path(r'^login/$',views.login,name='login'),
    re_path(r'^logout/$',views.logout,name='logout'),
    re_path(r'^history/$',views.history,name='history'),
    re_path(r'$',views.index,name='index'),
    path('sq/<str:id>/<str:sq_id>/', views.sq, name='sq'),
    path('bookmark/<str:id>/', views.bookmark, name='bm'),
    path('like/<str:id>/<str:click>/', views.like, name='like'),
    path('bookmarked_videos/', views.bookmarked_videos, name='bookmark'),
    path('trending/', views.trending, name='trending'),
]