from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.budget, name='budget'),
    url(r'^envelopes/', views.envelopes, name='envelopes'),
    url(r'^accounts/', views.accounts, name='accounts'),
    url(r'^goals/', views.goals, name='goals'),
    url(r'^my_spending/', views.my_spending, name='my_spending'),
    # url(r'^envelopes/', views.envelopes, name='envelopes'),
]
