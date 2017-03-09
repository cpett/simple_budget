from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sign_up/', views.sign_up, name='sign_up'),
    url(r'^login/', views.login, name='login'),
    url(r'^sign_out/', views.sign_out, name='sign_out'),
]
