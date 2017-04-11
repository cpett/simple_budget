from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.budget, name='budget'),
    url(r'^envelopes/', views.envelopes, name='envelopes'),
    url(r'^envelopes_edit/(\d+)/', views.envelopes_edit, name='envelopes_edit'),
    url(r'^accounts_add/', views.accounts_add, name='accounts_add'),
    url(r'^accounts_edit/(\d+)/', views.accounts_edit, name='accounts_edit'),
    url(r'^accounts_remove_confirm/(\d+)/', views.accounts_remove_confirm, name='accounts_remove_confirm'),
    url(r'^accounts_remove/(\d+)/', views.accounts_remove, name='accounts_remove'),
    url(r'^accounts/', views.accounts, name='accounts'),
    url(r'^goals_add/', views.goals_add, name='goals_add'),
    url(r'^goals_edit/(\d+)/', views.goals_edit, name='goals_edit'),
    url(r'^goals_remove_confirm/(\d+)/', views.goals_remove_confirm, name='goals_remove_confirm'),
    url(r'^goals_remove/(\d+)/', views.goals_remove, name='goals_remove'),
    url(r'^goals/', views.goals, name='goals'),
    url(r'^transactions/', views.transactions, name='transactions'),
    url(r'^transactions_add/', views.transactions_add, name='transactions_add'),
    url(r'^transactions_edit/(\d+)/', views.transactions_edit, name='transactions_edit'),
    url(r'^transactions_remove_confirm/(\d+)/', views.transactions_remove_confirm, name='transactions_remove_confirm'),
    url(r'^transactions_remove/(\d+)/', views.transactions_remove, name='transactions_remove'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^premium/', views.premium, name='premium'),
]
