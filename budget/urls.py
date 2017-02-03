from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.budget, name='budget'),
    url(r'^envelopes/', views.envelopes, name='envelopes'),
    url(r'^accounts_add/', views.accounts_add, name='accounts_add'),
    url(r'^accounts_edit/(\d+)', views.accounts_edit, name='accounts_edit'),
    url(r'^accounts_remove_confirm/(\d+)', views.accounts_remove_confirm, name='accounts_remove_confirm'),
    url(r'^accounts_remove/(\d+)', views.accounts_remove, name='accounts_remove'),
    url(r'^accounts/', views.accounts, name='accounts'),
    url(r'^goals_add/', views.goals_add, name='goals_add'),
    url(r'^goals_edit/(\d+)', views.goals_edit, name='goals_edit'),
    url(r'^goals_remove_confirm/(\d+)', views.goals_remove_confirm, name='goals_remove_confirm'),
    url(r'^goals_remove/(\d+)', views.goals_remove, name='goals_remove'),
    url(r'^goals/', views.goals, name='goals'),
    url(r'^my_spending/', views.my_spending, name='my_spending'),
    url(r'^settings/', views.settings, name='settings'),
]
