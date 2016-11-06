from django.shortcuts import render
from django.http import HttpResponse


def budget(request):
    '''
        Loads the progress/landing page for budget
    '''
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``')
    return render(request, 'budget.html')


def envelopes(request):
    '''
        Loads the envelopes page
    '''
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>')
    return render(request, 'envelopes.html')


def accounts(request):
    '''
        Loads the index/home page
    '''
    return render(request, 'accounts.html')


def goals(request):
    '''
        Loads the index/home page
    '''
    return render(request, 'goals.html')


def my_spending(request):
    '''
        Loads the index/home page
    '''
    return render(request, 'my_spending.html')
