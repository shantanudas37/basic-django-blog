__author__ = 'Shantanu'
from django.conf.urls import url
from posts import views as posts_views
from django.contrib import admin

urlpatterns = [
    url(r'^$', posts_views.post_list, name="list"), # works like this in django 1.10
    url(r'^create/$', posts_views.post_create, name="post_create"), # always cosider top url ifsame url pointing different method
    url(r'^(?P<slug>[\w-]+)/$', posts_views.post_detail, name="detail"),
    url(r'^(?P<slug>[\w-]+)/update/$', posts_views.post_update, name="update"),
    url(r'^(?P<id>\d+)/delete/$', posts_views.post_delete, name="delete"),
]