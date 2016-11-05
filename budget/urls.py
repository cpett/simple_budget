from django.conf.urls import url

from budget import views

urlpatterns = [
    url(r'^', views.budget, name='budget'),
    # url(r'^sign_up/', views.sign_up, name='sign_up'),
    # url(r'^sign_in/', views.sign_in, name='sign_in'),
]
