from django.shortcuts import render
from django.http import HttpResponse


def budget(request):
    '''
        Loads the index/home page
    '''
    return render(request, 'budget.html')
