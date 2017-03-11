from django import forms
from django.forms import ModelForm, PasswordInput, RadioSelect, DateInput, ModelChoiceField, extras
import urllib
import json, requests

from material import *

class UserForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput, min_length=8)
    password_confirmation = forms.CharField(required=True, label='Confirm password', widget=forms.PasswordInput, min_length=8)
    email = forms.EmailField(required=True)
    token = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        clean = True

        if password != password_confirmation:
            msg = "Both passwords must match"
            self.add_error('password', msg)
            self.add_error('password_confirmation', msg)
            clean = False
        if password and password == password_confirmation:
            if str(first_name).lower() in str(password).lower() or str(last_name).lower() in str(password).lower():
                            msg = "Passwords should not contain your name"
                            self.add_error('password', msg)
                            self.add_error('password_confirmation', msg)
                            clean = False
        if password and first_name and last_name and email:
            if clean == True:
                data = {
                          "user": {
                                    "first_name": first_name,
                                    "last_name": last_name,
                                    "email": email,
                                    "password": password,
                                    "password_confirmation": password_confirmation
                                  }
                         }
                path = 'https://simplifiapi.herokuapp.com/users'
                header = {'Content-type': 'application/json'}
                req = requests.post(path, data=json.dumps(data), headers=header)
                data = req.json()
                if req.ok is True:
                    self.cleaned_data['token'] = data['token']
                if 'email' in data:
                    if data['email'][0] == "has already been taken":
                        msg = 'It looks like we already have an account with this email'
                        self.add_error('email', msg)

    layout = Layout(
                    Fieldset("Create Account",
                             Row('first_name', 'last_name'),
                             Row('email'),
                             Row('password', 'password_confirmation')
                            )
                    )

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    token = forms.CharField(required=False)
    first_name = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            review = {
                'email': email,
                'password': password
            }
            mydata = urllib.parse.urlencode(review)
            mydata = mydata.encode('utf-8')
            path = 'https://simplifiapi.herokuapp.com/login'
            req = urllib.request.Request(path, mydata)
            try:
                response = urllib.request.urlopen(req)
                data = response.read().decode('utf-8')
                data = json.loads(data)
                self.cleaned_data['token'] = data['token']
                self.cleaned_data['first_name'] = data['first_name']
                return self.cleaned_data
            except:
                raise forms.ValidationError("Please check your credentials, and try again.")
    layout = Layout(
                    Fieldset("Sign In",
                             Row('email'),
                             Row('password')
                            )
                    )

class AccountForm(forms.Form):
    account_name = forms.CharField(max_length=25)
    account_types = (
                        ('checking', 'Checking'),
                        ('credit', 'Credit Card'),
                        ('investment', 'Investments'),
                        ('loan', 'Loan'),
                        ('savings', 'Savings'),
                    )
    account_type = forms.ChoiceField(choices=account_types)
    account_username = forms.CharField(help_text="Username for the financial institution")
    account_password = forms.CharField(help_text="Password for the financial institution",
                                       widget=forms.PasswordInput)
    layout = Layout(
                     Fieldset("Account Information",
                                Row('account_name', 'account_type')
                             ),
                     Fieldset("Account Credentials",
                                Row('account_username', 'account_password')
                             )
                    )

class TransactionForm(forms.Form):
    transaction_name = forms.CharField(max_length=25, label="Name")
    transaction_amount = forms.DecimalField(decimal_places=2, label="Amount")
    transaction_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}), label="Completion date")
    transaction_notes = forms.CharField(max_length=255, required=False)


class GoalForm(forms.Form):
    goal_name = forms.CharField(max_length=25, label="Name")
    goal_amount = forms.DecimalField(decimal_places=2, label="Amount")
    goal_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}), label="Completion date")
    goal_notes = forms.CharField(max_length=255, required=False)
    # widgets = {
    #     'goal_date': DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
    #     'goal_type': forms.RadioSelect(),
    # }

    layout = Layout(
                    Fieldset("Goal Information",
                             Row('goal_name'),
                             Row('goal_amount', 'goal_date'),
                             Row('goal_notes')
                            )
                    )
