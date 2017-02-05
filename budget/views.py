from django.shortcuts import render
from django.http import HttpResponse
from homepage import forms as frm
from homepage import models as mod
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


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
    if request.method == "POST":
        form = frm.AccountForm(request.POST)
        if form.is_valid():
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
def accounts_edit(request, account_id):
    '''
        Loads the the modal to edit an account
    '''
    if request.user.is_authenticated():
        user = request.user
    try:
        account = mod.Account.objects.get(user=user.id, pk=account_id)
    except ObjectDoesNotExist:
        context = {'error': 'error'}
        return render(request, 'accounts_edit.html', context)
    if request.method == "POST":
        form = frm.AccountForm(request.POST, instance=account)
        if form.is_valid():
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
        form = frm.AccountForm(instance=account)
    context = {'form': form,
               'account_id': account_id
              }
    return render(request, 'accounts_edit.html', context)

@login_required(login_url='/')
def accounts_remove_confirm(request, account_id):
    '''
        Loads the the modal to add new account
    '''
    try:
        account = mod.Account.objects.get(user=request.user.id, pk=account_id)
        context = {'account': account}
    except ObjectDoesNotExist:
        print('The selected object does not exist')
        error = 'Error'
        context = {'error': error}
    return render(request, 'accounts_remove.html', context)


@login_required(login_url='/')
def accounts_remove(request, account_id):
    '''
        Loads the the modal to add new account
    '''
    try:
        account = mod.Account.objects.get(user=request.user.id, pk=account_id)
        account.delete()
        return HttpResponse('success')
    except ObjectDoesNotExist:
        print('The selected object does not exist')
        return HttpResponse('error')
    return render(request, 'accounts_remove.html')

################################
############ GOALS ############
###############################
@login_required(login_url='/')
def goals(request):
    '''
        Loads the goals page
    '''
    if request.user.is_authenticated():
        user = request.user
    goal_count = mod.Goal.objects.all() \
                    .filter(user=user) \
                    .count()
    goals = mod.Goal.objects.all() \
                    .filter(user=user)
    context = {'goals': goals,
                'goal_count' : goal_count,
              }
    return render(request, 'goals.html', context)

@login_required(login_url='/')
def goals_add(request):
    '''
        Loads the the modal to add new goal
    '''
    if request.user.is_authenticated():
        user = request.user
    if request.method == "POST":
        form = frm.GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = user
            goal.goal_name = form.cleaned_data['goal_name']
            goal.amount = form.cleaned_data['amount']
            goal.goal_date = form.cleaned_data['goal_date']
            goal.save()
            # TODO: fix this hack -- passes success to the AJAX success function
            # if it completed successfully
            return HttpResponse("success")
    else:
        form = frm.GoalForm()
    context = {'form': form}
    return render(request, 'goals_add.html', context)

    context = {'goals': goals,
                'goal_count': goal_count
              }
    return render(request, 'goals.html', context)

@login_required(login_url='/')
def goals_add(request):
    '''
        Loads the the modal to add new goal
    '''
    if request.user.is_authenticated():
        user = request.user
    if request.method == "POST":
        form = frm.GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = user
            goal.goal_name = form.cleaned_data['goal_name']
            goal.amount = form.cleaned_data['amount']
            goal.goal_date = form.cleaned_data['goal_date']
            goal.save()
            # TODO: fix this hack -- passes success to the AJAX success function
            # if it completed successfully
            return HttpResponse("success")
    else:
        form = frm.GoalForm()
    context = {'form': form}
    return render(request, 'goals_add.html', context)

@login_required(login_url='/')
def goals_edit(request, goal_id):
    '''
        Loads the the modal to edit a goal
    '''
    if request.user.is_authenticated():
        user = request.user
    try:
        goal = mod.Goal.objects.get(user=user.id, pk=goal_id)
    except ObjectDoesNotExist:
        context = {'error': 'error'}
        return render(request, 'goals_edit.html', context)
    if request.method == "POST":
        form = frm.GoalForm(request.POST, instance=goal)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = user
            goal.goal_name = form.cleaned_data['goal_name']
            goal.amount = form.cleaned_data['amount']
            goal.goal_date = form.cleaned_data['goal_date']
            goal.save()
            # TODO: fix this hack -- passes success to the AJAX success function
            # if it completed successfully
            return HttpResponse("success")
    else:
        form = frm.GoalForm(instance=goal)
    context = {'form': form,
               'goal_id': goal_id
              }
    return render(request, 'goals_edit.html', context)

@login_required(login_url='/')
def goals_remove_confirm(request, goal_id):
    '''
        Loads the the modal to remove goal
    '''
    try:
        goal = mod.Goal.objects.get(user=request.user.id, pk=goal_id)
        context = {'goal': goal}
    except ObjectDoesNotExist:
        print('The selected object does not exist')
        error = 'Error'
        context = {'error': error}
    return render(request, 'goals_remove.html', context)


@login_required(login_url='/')
def goals_remove(request, goal_id):
    '''
        Loads the the modal to remove goal
    '''
    try:
        goal = mod.Goal.objects.get(user=request.user.id, pk=goal_id)
        goal.delete()
        return HttpResponse('success')
    except ObjectDoesNotExist:
        print('The selected object does not exist')
        return HttpResponse('error')
    return render(request, 'goals_remove.html')


################################
######## Transactions #########
###############################
@login_required(login_url='/')
def transactions(request):
    '''
        Loads the my spending page
    '''
    if request.user.is_authenticated():
        user = request.user
    user_accounts = mod.Account.objects.all().filter(user=user)
    transaction_count = mod.Transaction.objects.all() \
                    .filter(account__in=user_accounts) \
                    .count()
    transactions = mod.Transaction.objects.all() \
                    .filter(account__in=user_accounts)

    context = {'transaction_count': transaction_count,
               'transactions': transactions,
              }
    return render(request, 'transactions.html', context)


@login_required(login_url='/')
def transactions_add(request):
    '''
        Loads the the modal to add new transaction
    '''
    if request.user.is_authenticated():
        user = request.user
    if request.method == "POST":
        form = frm.TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = form.cleaned_data['account']
            transaction.category = form.cleaned_data['category']
            transaction.description = form.cleaned_data['description']
            transaction.original_description = form.cleaned_data['original_description']
            transaction.date = form.cleaned_data['date']
            transaction.amount = form.cleaned_data['amount']
            transaction.save()
            # TODO: fix this hack -- passes success to the AJAX success function
            # if it completed successfully
            return HttpResponse("success")
    else:
        form = frm.TransactionForm()
    context = {'form': form}
    return render(request, 'transactions_add.html', context)


@login_required(login_url='/')
def transactions_edit(request, transaction_id):
    '''
        Loads the the modal to edit an account
    '''
    if request.user.is_authenticated():
        user = request.user
    try:
        trans = mod.Transaction.objects.get(id=transaction_id)
    except ObjectDoesNotExist:
        context = {'error': 'error'}
        return render(request, 'transactions_edit.html', context)
    if request.method == "POST":
        print('>>>>>>>>>>>>> POST')
        form = frm.TransactionForm(request.POST, instance=trans)
        if form.is_valid():
            print('>>>>>>>>>>> VALID')
            transaction = form.save(commit=False)
            transaction.account = form.cleaned_data['account']
            transaction.category = form.cleaned_data['category']
            transaction.description = form.cleaned_data['description']
            transaction.original_description = form.cleaned_data['original_description']
            transaction.date = form.cleaned_data['date']
            transaction.amount = form.cleaned_data['amount']
            transaction.save()
            # TODO: fix this hack -- passes success to the AJAX success function
            # if it completed successfully
            return HttpResponse("success")
    else:
        form = frm.TransactionForm(instance=trans)
    context = {'form': form,
               'transaction_id': transaction_id
              }
    return render(request, 'transactions_edit.html', context)


@login_required(login_url='/')
def transactions_remove_confirm(request, transaction_id):
    '''
        Loads the the modal to add new account
    '''
    try:
        transaction = mod.Transaction.objects.get(id=transaction_id)
        context = {'transaction': transaction}
    except ObjectDoesNotExist:
        print('The selected object does not exist')
        error = 'Error'
        context = {'error': error}
    return render(request, 'transactions_remove.html', context)


@login_required(login_url='/')
def transactions_remove(request, transaction_id):
    '''
        Loads the the modal to add new account
    '''
    try:
        transaction = mod.Transaction.objects.get(id=transaction_id)
        transaction.delete()
        return HttpResponse('success')
    except ObjectDoesNotExist:
        print('The selected object does not exist')
        return HttpResponse('error')
    return render(request, 'transactions_remove.html')


@login_required(login_url='/')
def settings(request):
    '''
        Loads the my spending page
    '''
    return render(request, 'settings.html')
