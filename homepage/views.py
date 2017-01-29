from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from homepage import forms as frm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django import forms
from material import *

@csrf_protect
def index(request):
    '''
        Loads the index/home page
    '''
    return render(request, 'index.html')

@csrf_protect
def sign_up(request):
    '''
        Loads the modal for creating new accounts
    '''
    if request.method == "POST":
        form = frm.UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            # go ahead and authenticate the new user
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('success')
    else:
        form = frm.UserForm()
    context = {'form': form}
    return render(request, 'sign_up.html', context)

@csrf_protect
def sign_in(request):
    '''
        Loads the modal for logging in
    '''
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                # TODO: FIX this hack with the AJAX success function
                return HttpResponse('success')

    context = {'form': form}
    return render(request, 'sign_in.html', context)


def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')
