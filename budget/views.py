from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from homepage import forms as frm
from homepage import models as mod
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
import datetime
import dateutil.parser
from decimal import Decimal


def parser(json_data):
    '''Parse json data for template'''
    result_data = {}
    result_data['data'] = json_data
    dump_data = json.dumps(result_data)
    return json.loads(dump_data)


def check_login(function):
  def wrap(request, *args, **kwargs):
    if not request.session.get('api_token'):
        print('No token in the session')
        return HttpResponseRedirect('/')
    else:
        token = 'Token token=' + request.session.get('api_token')
        path = 'https://simplifiapi2.herokuapp.com/users'
        req = requests.get(path, headers={'Authorization': token})
        if req.ok is False:
            print('token exists, but expired')
            return HttpResponseRedirect('/sign_out/')
        else:
            print('All good in the hood')
            return function(request, *args, **kwargs)
  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap

@check_login
def budget(request):
    '''
        Loads the progress/landing page for budget
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/accounts'
    req = requests.get(path, headers={'Authorization': token})
    data = req.json()
    load_data = parser(data)
    total = 0
    for d in load_data['data']:
        if d['available_balance'] != None:
            total += d['available_balance']

    data = []
    donations = ["Donations",10]
    education = ["Education",10]
    entertainment = ["Entertainment",10]
    fees = ["Fees",10]
    food = ["Food", 2.5, 1.9, 2.1, 1.8, 2.2, 2.1, 1.7, 1.8, 1.8, 2.5, 2.0, 1.9, 2.1, 2.0, 2.4, 2.3, 1.8, 2.2, 2.3, 1.5, 2.3, 2.0, 2.0, 1.8, 2.1, 1.8, 1.8, 1.8, 2.1, 1.6, 1.9, 2.0, 2.2, 1.5, 1.4, 2.3, 2.4, 1.8, 1.8, 2.1, 2.4, 2.3, 1.9, 2.3, 2.5, 2.3, 1.9, 2.0, 2.3, 1.8]
    health = ["Health",10]
    home = ["Home", 1.4, 1.5, 1.5, 1.3, 1.5, 1.3, 1.6, 1.0, 1.3, 1.4, 1.0, 1.5, 1.0, 1.4, 1.3, 1.4, 1.5, 1.0, 1.5, 1.1, 1.8, 1.3, 1.5, 1.2, 1.3, 1.4, 1.4, 1.7, 1.5, 1.0, 1.1, 1.0, 1.2, 1.6, 1.5, 1.6, 1.5, 1.3, 1.3, 1.3, 1.2, 1.4, 1.2, 1.0, 1.3, 1.2, 1.3, 1.3, 1.1, 1.3]
    insurance = ["Insurance",10]
    payments = ["Payments",10]
    professional = ["Professional Services",10]
    miscellaneous = ["Miscellaneous",10]
    shopping = ["Shopping",10]
    subscriptions = ["Subscriptions",10]
    travel = ["Travel", 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.3, 0.2, 0.2, 0.1, 0.2, 0.2, 0.1, 0.1, 0.2, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.4, 0.2, 0.5, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.6, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2]
    other = ["Other",10]
    doughnutData = [donations, education, entertainment, fees, food, health, home, insurance, payments, professional, miscellaneous, shopping, subscriptions, travel, other]
    context = {"doughnutData" : doughnutData, "total" : total}
    return render(request, 'budget.html', context)

@check_login
def envelopes(request):
    '''
        Loads the envelopes page
    '''
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/user_envelopes'
    req = requests.get(path, headers={'Authorization': token})
    data = req.json()
    data = sorted(data, key=lambda x:x['envelope_name'].upper())
    load_data = parser(data)
    data = json.dumps(load_data['data'])

    context = {'envelopes': load_data['data'], 'data':data}
    if request.GET.get('type'):
        return render(request, 'envelopes_ajax.html', context)
    else:
        return render(request, 'envelopes.html', context)

@check_login
def envelopes_edit(request, env_id):
    '''
        Edit Envelope amount
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/user_envelopes/' + env_id
    req = requests.get(path, headers={'Authorization': token})
    data = req.json()

    if request.method == "POST":
        form = frm.EnvelopeForm(request.POST)
        if form.is_valid():
            token = 'Token token=' + request.session.get('api_token')
            path = 'https://simplifiapi2.herokuapp.com/user_envelopes/' + env_id
            data = {
                    "amount":float(form.cleaned_data['amount']),
                    "id":env_id
                   }
            header = {'Content-type': 'application/json', 'Authorization': token}
            req = requests.put(path, data=json.dumps(data), headers=header)
            if req.ok is False:
                return render(request, 'envelopes_edit.html', {'error':req.status_code})
            return HttpResponse("success")
        else:
            context = {'form':form, 'name': data['envelope_name'], 'amount':data['amount']}
            return render(request, 'envelopes_add_ajax.html', )
    else:
        form = frm.EnvelopeForm({'amount': data['amount']})
    context = {'form': form, 'name': data['envelope_name'], 'amount':data['amount'], 'envelope_id': env_id}
    return render(request, 'envelopes_edit.html', context)

################################
########## ACCOUNTS ###########
###############################
@check_login
def accounts(request):
    '''
        Loads the accounts page
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/accounts'
    req = requests.get(path, headers={'Authorization': token})
    data = req.json()
    data = sorted(data, key=lambda x:x['name'].upper())
    load_data = parser(data)
    balance = 0
    for d in load_data['data']:
        if d['account_subtype'] != 'credit':
            if d['available_balance'] != None:
                balance += d['available_balance']
            elif d['current_balance']:
                balance += d['current_balance']
        else:
            balance -= d['current_balance']

    context = {'accounts': load_data['data'], 'balance': balance}
    if request.GET.get('type'):
        return render(request, 'accounts_ajax.html', context)
    else:
        return render(request, 'accounts.html', context)


@check_login
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
            path = 'https://simplifiapi2.herokuapp.com/accounts'
            data = {
                    "name":form.cleaned_data['account_name'],
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


@check_login
def accounts_edit(request, account_id):
    '''
        Loads the the modal to edit an account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and pre-populate form with API data
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/accounts/' + account_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.get(path, headers=header)
    if req.ok is False:
        return render(request, 'accounts_edit.html', {'error':req.status_code})
    data = req.json()
    if request.method == "POST":
        form = frm.AccountForm(request.POST)
        if form.is_valid():
            token = 'Token token=' + request.session.get('api_token')
            path = 'https://simplifiapi2.herokuapp.com/accounts/' + account_id
            data = {
                    "name":form.cleaned_data['account_name'],
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
                                'account_name': data['name'],
                                'account_password': data['account_password']
                               })
    context = {'form': form, 'account_id': account_id}
    return render(request, 'accounts_edit.html', context)

@check_login
def accounts_remove_confirm(request, account_id):
    '''
        Loads the the modal to delete an account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and account for deletion
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/accounts/' + account_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.get(path, headers=header)
    if req.ok is False:
        context = {'error': req.status_code}
    else:
        data = req.json()
        load_data = parser(data)
        context = {'account': load_data['data']}
    return render(request, 'accounts_remove.html', context)


@check_login
def accounts_remove(request, account_id):
    '''
        Deletes the selected account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and account for deletion
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/accounts/' + account_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.delete(path, headers=header)
    if req.ok is False:
        return render(request, 'accounts_remove_ajax.html', {'error': req.status_code})
    else:
        return HttpResponse("success")


################################
############ GOALS ############
###############################
@check_login
def goals(request):
    '''
        Loads the goals page
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/goals'
    req = requests.get(path, headers={'Authorization': token})
    data = req.json()
    data = sorted(data, key=lambda x:x['name'].upper())
    load_data = parser(data)

    context = {'goals': load_data['data']}
    if request.GET.get('type'):
        return render(request, 'goals_ajax.html', context)
    else:
        return render(request, 'goals.html', context)

@check_login
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
            path = 'https://simplifiapi2.herokuapp.com/goals'
            data = {
                    "name":form.cleaned_data['name'],
                    "amount":int(form.cleaned_data['amount']),
                    "date":str(form.cleaned_data['date']),
                    "note":form.cleaned_data['note'],
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

@check_login
def goals_edit(request, goal_id):
    '''
        Loads the the modal to edit a goal
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and pre-populate form with API data
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/goals/' + goal_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.get(path, headers=header)
    if req.ok is False:
        return render(request, 'goals_edit.html', {'error':req.status_code})
    data = req.json()
    if request.method == "POST":
        form = frm.GoalForm(request.POST)
        if form.is_valid():
            data = {
                    "name":form.cleaned_data['name'],
                    "amount":int(form.cleaned_data['amount']),
                    "date":str(form.cleaned_data['date']),
                    "note":form.cleaned_data['note'],
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
        date = dateutil.parser.parse(data['date']).strftime('%Y-%m-%d')
        form = frm.GoalForm({'name': data['name'],
                             'amount': data['amount'],
                             'date': date,
                             'note': data['note']
                           })
    context = {'form': form, 'goal_id': goal_id}
    return render(request, 'goals_edit.html', context)

@check_login
def goals_remove_confirm(request, goal_id):
    '''
        Loads the the modal to remove goal
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/goals/' + goal_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.get(path, headers=header)
    if req.ok is False:
        context = {'error': req.status_code}
    else:
        data = req.json()
        load_data = parser(data)
        context = {'goal': load_data['data']}
    return render(request, 'goals_remove.html', context)


@check_login
def goals_remove(request, goal_id):
    '''
        Loads the the modal to remove goal
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and goal for deletion
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/goals/' + goal_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.delete(path, headers=header)
    if req.ok is False:
        return render(request, 'goals_remove_ajax.html', {'error': req.status_code})
    else:
        return HttpResponse("success")


################################
######## Transactions #########
###############################
@check_login
def transactions(request):
    '''
        Loads the my spending page
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/account_transactions'
    req = requests.get(path, headers={'Authorization': token})
    data = req.json()
    data = sorted(data, key=lambda x:x['date'].upper())
    load_data = parser(data)

    context = {'transactions': load_data['data']}
    if request.GET.get('type'):
        return render(request, 'transactions_ajax.html', context)
    else:
        return render(request, 'transactions.html', context)

@check_login
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
            path = 'https://simplifiapi2.herokuapp.com/account_transactions'
            data = {
                    "date":str(form.cleaned_data['transaction_date']),
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


@check_login
def transactions_edit(request, transaction_id):
    '''
        Loads the the modal to edit an account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and pre-populate form with API data
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/account_transactions/' + transaction_id
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
            path = 'https://simplifiapi2.herokuapp.com/account_transactions/' + transaction_id
            data = {
                    "date":str(form.cleaned_data['transaction_date']),
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
        # import dateutil.parser
        # date = dateutil.parser.parse(data['date'])
        if Decimal(data['amount']) < 0:
            transaction_type = '1'
        else:
            transaction_type = '2'
        form = frm.TransactionForm(request,
                                   initial={
                                            'transaction_type':transaction_type,
                                            'transaction_date':data['date'],
                                            'transaction_amount':data['amount'],
                                            'category':62,# data['category_name'],
                                            'account':322# data['account_name']
                                           }
                                  )
    context = {'form': form,'transaction_id': transaction_id}
    return render(request, 'transactions_edit.html', context)


@check_login
def transactions_remove_confirm(request, transaction_id):
    '''
        Loads the the modal to add new account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and transaction for deletion
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/account_transactions/' + transaction_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.get(path, headers=header)
    if req.ok is False:
        context = {'error': req.status_code}
    else:
        data = req.json()
        load_data = parser(data)
        context = {'transaction': load_data['data']}
    return render(request, 'transactions_remove.html', context)


@check_login
def transactions_remove(request, transaction_id):
    '''
        Loads the the modal to add new account
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    # Get token and transaction for deletion
    token = 'Token token=' + request.session.get('api_token')
    path = 'https://simplifiapi2.herokuapp.com/account_transactions/' + transaction_id
    header = {'Content-type': 'application/json', 'Authorization': token}
    req = requests.delete(path, headers=header)
    if req.ok is False:
        return render(request, 'transactions_remove_ajax.html', {'error': req.status_code})
    else:
        return HttpResponse("success")

@check_login
def settings(request):
    '''
        Loads the my spending page
    '''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    return render(request, 'settings.html')

def premium(request):
    '''Warns about a premium feature'''
    if not request.session.get('api_token'):
        return HttpResponseRedirect('/')
    return render(request, 'premium.html')
