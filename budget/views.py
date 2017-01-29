from django.shortcuts import render
from django.http import HttpResponse
from homepage import forms as frm
from homepage import models as mod
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def budget(request):
    '''
        Loads the progress/landing page for budget
    '''
    return render(request, 'budget.html')

@login_required(login_url='/')
def envelopes(request):
    '''
        Loads the envelopes page
    '''
    return render(request, 'envelopes.html')

################################
########## ACCOUNTS ###########
###############################
@login_required(login_url='/')
def accounts(request):
    '''
        Loads the accounts page
    '''
    if request.user.is_authenticated():
        user = request.user
    account_count = mod.Account.objects.all() \
                    .filter(user=user) \
                    .count()
    checkings = mod.Account.objects.all() \
                    .filter(user=user, acc_type='CH')
    credits = mod.Account.objects.all() \
                    .filter(user=user, acc_type='CC')
    invests = mod.Account.objects.all() \
                    .filter(user=user, acc_type='IN')
    savings = mod.Account.objects.all() \
                    .filter(user=user, acc_type='SV')
    loans = mod.Account.objects.all() \
                    .filter(user=user, acc_type='LN')
    context = {'checkings': checkings,
               'account_count': account_count,
               'credits': credits,
               'invests': invests,
               'savings': savings,
              }
    return render(request, 'accounts.html', context)


@login_required(login_url='/')
def accounts_add(request):
    '''
        Loads the the modal to add new account
    '''
    if request.user.is_authenticated():
        user = request.user
        print(user)
    if request.method == "POST":
        form = frm.AccountForm(request.POST)
        print('POSTED!')
        if form.is_valid():
            print('VALID!')
            account = form.save(commit=False)
            account.user = user
            account.account_name = form.cleaned_data['account_name']
            account.acc_type = form.cleaned_data['acc_type']
            # Need to see how to best handle 3rd party credentials
            account.acc_password = form.cleaned_data['acc_password']
            account.acc_username = form.cleaned_data['acc_username']
            account.save()
            # TODO: fix this hack -- passes success to the AJAX success function
            # if it completed successfully
            return HttpResponse("success")
    else:
        form = frm.AccountForm()
    context = {'form': form}
    return render(request, 'accounts_add.html', context)


@login_required(login_url='/')
def accounts_remove(request):
    '''
        Loads the the modal to add new account
    '''
    return render(request, 'accounts_remove.html')


@login_required(login_url='/')
def goals(request):
    '''
        Loads the goals page
    '''
    return render(request, 'goals.html')


@login_required(login_url='/')
def my_spending(request):
    '''
        Loads the my spending page
    '''
    return render(request, 'my_spending.html')


@login_required(login_url='/')
def settings(request):
    '''
        Loads the my spending page
    '''
    return render(request, 'settings.html')
