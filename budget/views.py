from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    '''
        Loads the index/home page
    '''
    return render(request, 'index.html')


def sign_up(request):
    '''
        Loads the page with all the Tableau things
    '''
    return render(request, 'sign_up.html')
