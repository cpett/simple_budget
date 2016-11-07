from django.shortcuts import render
from django.http import HttpResponse


def budget(request):
    '''
        Loads the progress/landing page for budget
    '''
    return render(request, 'budget.html')


def envelopes(request):
    '''
        Loads the envelopes page
    '''
    return render(request, 'envelopes.html')


def accounts(request):
    '''
        Loads the accounts page
    '''
    return render(request, 'accounts.html')


def goals(request):
    '''
        Loads the goals page
    '''
    return render(request, 'goals.html')


def my_spending(request):
    '''
        Loads the my spending page
    '''
    return render(request, 'my_spending.html')


def settings(request):
    '''
        Loads the my spending page
    '''
    return render(request, 'settings.html')
