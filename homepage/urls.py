from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sign_up/', views.sign_up, name='sign_up'),
    url(r'^sign_in/', views.sign_in, name='sign_in'),
]