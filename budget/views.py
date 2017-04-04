from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from homepage import forms as frm
from homepage import models as mod
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
import datetime
from decimal import Decimal
from plaid import Client


def parser(json_data):
    '''Parse json data for template'''
    result_data = {}
    result_data['data'] = json_data
    dump_data = json.dumps(result_data)
    return json.loads(dump_data)


# @login_required(login_url='/')
def budget(request):
    '''
        Loads the progress/landing page for budget
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    return render(request, 'budget.html')

# @login_required(login_url='/')
def envelopes(request):
    '''
        Loads the envelopes page
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    return render(request, 'envelopes.html')

################################
########## ACCOUNTS ###########
###############################
# @login_required(login_url='/')
def accounts(request):
    '''
        Loads the accounts page
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi.herokuapp.com/accounts'
    req = requests.get(path, headers={'Authorization': token})
    data = req.json()
    data = sorted(data, key=lambda x:x['institution_name'].upper())
    load_data = parser(data)
    print(load_data['data'])
    context = {'accounts': load_data['data']}
    if request.GET.get('type'):
        return render(request, 'accounts_ajax.html', context)
    else:
        return render(request, 'accounts.html', context)


# @login_required(login_url='/')
def accounts_add(request):
    '''
        Loads the the modal to add new account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    if request.method == "POST":
        form = frm.AccountForm(request.POST)
        if form.is_valid():
            token = 'Token token=' + request.session.get('api_token')
            path = 'https://simplifiapi.herokuapp.com/accounts'
            data = {
                    "institution_name":form.cleaned_data['account_name'],
                    "account_type":form.cleaned_data['account_type'],
                    "account_username":form.cleaned_data['account_username'],
                    "account_password":form.cleaned_data['account_password'],
                   }
            header = {'Content-type': 'application/json', 'Authorization': token}
            req = requests.post(path, data=json.dumps(data), headers=header)
            if req.ok is False:
                return render(request, 'accounts_edit.html', {'error':req.status_code})
            return HttpResponse("success")
        else:
            return render(request, 'accounts_add_ajax.html', {'form':form})
    else:
        form = frm.AccountForm()
    context = {'form': form}
    return render(request, 'accounts_add.html', context)


# @login_required(login_url='/')
def accounts_edit(request, account_id):
    '''
        Loads the the modal to edit an account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and pre-populate form with API data
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi.herokuapp.com/accounts/' + account_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.get(path, headers=header)
    if req.ok is False:
        return render(request, 'accounts_edit.html', {'error':req.status_code})
    data = req.json()
    if request.method == "POST":
        form = frm.AccountForm(request.POST)
        if form.is_valid():
            token = 'Token token=' + request.session.get('api_token')
            path = 'https://simplifiapi.herokuapp.com/accounts/' + account_id
            data = {
                    "institution_name":form.cleaned_data['account_name'],
                    "account_type":form.cleaned_data['account_type'],
                    "account_username":form.cleaned_data['account_username'],
                    "account_password":form.cleaned_data['account_password'],
                   }
            header = {'Content-type': 'application/json', 'Authorization': token}
            # Update db instance
            req = requests.put(path, data=json.dumps(data), headers=header)
            if req.ok is False:
                return render(request, 'accounts_edit.html', {'error':req.status_code})
            return HttpResponse("success")
        else:
            context = {'form':form, 'account_id': account_id}
            return render(request, 'accounts_edit_ajax.html', context)
    else:
        form = frm.AccountForm({'account_username': data['account_username'],
                                'account_type': data['account_type'],
                                'account_name': data['institution_name'],
                                'account_password': data['account_password']
                               })
    context = {'form': form, 'account_id': account_id}
    return render(request, 'accounts_edit.html', context)

# @login_required(login_url='/')
def accounts_remove_confirm(request, account_id):
    '''
        Loads the the modal to delete an account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and account for deletion
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi.herokuapp.com/accounts/' + account_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.get(path, headers=header)
    if req.ok is False:
        context = {'error': req.status_code}
    else:
        data = req.json()
        load_data = parser(data)
        context = {'account': load_data['data']}
    return render(request, 'accounts_remove.html', context)


# @login_required(login_url='/')
def accounts_remove(request, account_id):
    '''
        Deletes the selected account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and account for deletion
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi.herokuapp.com/accounts/' + account_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.delete(path, headers=header)
    if req.ok is False:
        return render(request, 'accounts_remove_ajax.html', {'error': req.status_code})
    else:
        return HttpResponse("success")


################################
############ GOALS ############
###############################
# @login_required(login_url='/')
def goals(request):
    '''
        Loads the goals page
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi.herokuapp.com/goals'
    req = requests.get(path, headers={'Authorization': token})
    data = req.json()
    data = sorted(data, key=lambda x:x['goal_name'].upper())
    load_data = parser(data)

    context = {'goals': load_data['data']}
    if request.GET.get('type'):
        return render(request, 'goals_ajax.html', context)
    else:
        return render(request, 'goals.html', context)

# @login_required(login_url='/')
def goals_add(request):
    '''
        Loads the the modal to add new goal
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    if request.method == "POST":
        form = frm.GoalForm(request.POST)
        if form.is_valid():
            token = 'Token token=' + request.session.get('api_token')
            path = 'https://simplifiapi.herokuapp.com/goals'
            data = {
                    "goal_name":form.cleaned_data['goal_name'],
                    "goal_amount":int(form.cleaned_data['goal_amount']),
                    "goal_date":str(form.cleaned_data['goal_date']),
                    "goal_note":form.cleaned_data['goal_note'],
                   }
            header = {'Content-type': 'application/json', 'Authorization': token}
            req = requests.post(path, data=json.dumps(data), headers=header)
            if req.ok is False:
                return render(request, 'goals_edit.html', {'error':req.status_code})
            return HttpResponse("success")
        else:
            return render(request, 'goals_add_ajax.html', {'form':form})
    else:
        form = frm.GoalForm()
    context = {'form': form}
    return render(request, 'goals_add.html', context)

    context = {'goals': goals}
    return render(request, 'goals.html', context)


# @login_required(login_url='/')
def goals_edit(request, goal_id):
    '''
        Loads the the modal to edit a goal
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and pre-populate form with API data
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi.herokuapp.com/goals/' + goal_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.get(path, headers=header)
    if req.ok is False:
        return render(request, 'goals_edit.html', {'error':req.status_code})
    data = req.json()
    if request.method == "POST":
        form = frm.GoalForm(request.POST)
        if form.is_valid():
            data = {
                    "goal_name":form.cleaned_data['goal_name'],
                    "goal_amount":int(form.cleaned_data['goal_amount']),
                    "goal_date":str(form.cleaned_data['goal_date']),
                    "goal_note":form.cleaned_data['goal_note'],
                   }
            header = {'Content-type': 'application/json', 'Authorization': token}
            req = requests.put(path, data=json.dumps(data), headers=header)
            if req.ok is False:
                return render(request, 'goals_edit.html', {'error':req.status_code})
            return HttpResponse("success")
        else:
            context = {'form':form, 'goal_id': goal_id}
            return render(request, 'goals_edit_ajax.html', context)
    else:
        form = frm.GoalForm({'goal_name': data['goal_name'],
                             'goal_amount': data['goal_amount'],
                             'goal_date': data['goal_date'],
                             'goal_note': data['goal_note']
                           })
    context = {'form': form, 'goal_id': goal_id}
    return render(request, 'goals_edit.html', context)

# @login_required(login_url='/')
def goals_remove_confirm(request, goal_id):
    '''
        Loads the the modal to remove goal
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi.herokuapp.com/goals/' + goal_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.get(path, headers=header)
    if req.ok is False:
        context = {'error': req.status_code}
    else:
        data = req.json()
        load_data = parser(data)
        context = {'goal': load_data['data']}
    return render(request, 'goals_remove.html', context)


# @login_required(login_url='/')
def goals_remove(request, goal_id):
    '''
        Loads the the modal to remove goal
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and goal for deletion
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi.herokuapp.com/goals/' + goal_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.delete(path, headers=header)
    if req.ok is False:
        return render(request, 'goals_remove_ajax.html', {'error': req.status_code})
    else:
        return HttpResponse("success")


################################
######## Transactions #########
###############################
# @login_required(login_url='/')
def transactions(request):
    '''
        Loads the my spending page
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi.herokuapp.com/account_transactions'
    req = requests.get(path, headers={'Authorization': token})
    data = req.json()
    data = sorted(data, key=lambda x:x['transaction_date'].upper())
    load_data = parser(data)

    context = {'transactions': load_data['data']}
    if request.GET.get('type'):
        return render(request, 'transactions_ajax.html', context)
    else:
        return render(request, 'transactions.html', context)

# @login_required(login_url='/')
def transactions_add(request):
    '''
        Loads the the modal to add new transaction
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    if request.method == "POST":
        form = frm.TransactionForm(request, request.POST)
        if form.is_valid():
            amount = form.cleaned_data['transaction_amount']
            transaction_type = form.cleaned_data['transaction_type']
            if transaction_type == '1':
                if amount >= 0.00:
                    amount = amount * Decimal(-1)
            else:
                if amount < 0.00:
                    amount = amount * Decimal(-1)
            token = 'Token token=' + request.session.get('api_token')
            path = 'https://simplifiapi.herokuapp.com/account_transactions'
            data = {
                    "transaction_date":str(form.cleaned_data['transaction_date']),
                    "account_id":form.cleaned_data['account'],
                    "category_id":form.cleaned_data['category'],
                    "amount":str(amount)
                   }
            header = {'Content-type': 'application/json', 'Authorization': token}
            req = requests.post(path, data=json.dumps(data), headers=header)
            if req.ok is False:
                return render(request, 'transactions_add_ajax.html', {'error':req.status_code})
            return HttpResponse("success")
        else:
            return render(request, 'transactions_add_ajax.html', {'form':form})
    else:
        form = frm.TransactionForm(request, initial={'transaction_type':'1'})
    context = {'form': form}
    return render(request, 'transactions_add.html', context)


# @login_required(login_url='/')
def transactions_edit(request, transaction_id):
    '''
        Loads the the modal to edit an account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and pre-populate form with API data
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi.herokuapp.com/account_transactions/' + transaction_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.get(path, headers=header)
    if req.ok is False:
        return render(request, 'transactions_edit.html', {'error':req.status_code})
    data = req.json()
    if request.method == "POST":
        form = frm.TransactionForm(request, request.POST)
        if form.is_valid():
            amount = form.cleaned_data['transaction_amount']
            transaction_type = form.cleaned_data['transaction_type']
            if transaction_type == '1':
                if amount >= 0.00:
                    amount = amount * Decimal(-1)
            else:
                if amount < 0.00:
                    amount = amount * Decimal(-1)
            token = 'Token token=' + request.session.get('api_token')
            path = 'https://simplifiapi.herokuapp.com/account_transactions/' + transaction_id
            data = {
                    "transaction_date":str(form.cleaned_data['transaction_date']),
                    "account_id":form.cleaned_data['account'],
                    "category_id":form.cleaned_data['category'],
                    "amount":str(amount)
                   }
            header = {'Content-type': 'application/json', 'Authorization': token}
            req = requests.put(path, data=json.dumps(data), headers=header)
            if req.ok is False:
                return render(request, 'transactions_edit_ajax.html', {'error':req.status_code})
            return HttpResponse("success")
        else:
            return render(request, 'transactions_edit_ajax.html', {'form': form,'transaction_id': transaction_id})
    else:
        import dateutil.parser
        date = dateutil.parser.parse(data['transaction_date'])
        if Decimal(data['amount']) < 0:
            transaction_type = '1'
        else:
            transaction_type = '2'
        form = frm.TransactionForm(request,
                                   initial={
                                            'transaction_type':transaction_type,
                                            'transaction_date':date,
                                            'transaction_amount':data['amount'],
                                            'category':62,# data['category_name'],
                                            'account':322# data['account_name']
                                           }
                                  )
    context = {'form': form,'transaction_id': transaction_id}
    return render(request, 'transactions_edit.html', context)


# @login_required(login_url='/')
def transactions_remove_confirm(request, transaction_id):
    '''
        Loads the the modal to add new account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and transaction for deletion
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi.herokuapp.com/account_transactions/' + transaction_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.get(path, headers=header)
    if req.ok is False:
        context = {'error': req.status_code}
    else:
        data = req.json()
        load_data = parser(data)
        context = {'transaction': load_data['data']}
    return render(request, 'transactions_remove.html', context)


# @login_required(login_url='/')
def transactions_remove(request, transaction_id):
    '''
        Loads the the modal to add new account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and transaction for deletion
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi.herokuapp.com/account_transactions/' + transaction_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.delete(path, headers=header)
    if req.ok is False:
        return render(request, 'transactions_remove_ajax.html', {'error': req.status_code})
    else:
        return HttpResponse("success")

# @login_required(login_url='/')
def settings(request):
    '''
        Loads the my spending page
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    return render(request, 'settings.html')
