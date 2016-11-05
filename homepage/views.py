from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    '''
        Loads the index/home page
    '''
    return render(request, 'index.html')


def sign_up(request):
    '''
        Loads the modal for creating new accounts
    '''
    return render(request, 'sign_up.html')


def sign_in(request):
    '''
        Loads the modal for logging in
    '''
    return render(request, 'sign_in.html')
