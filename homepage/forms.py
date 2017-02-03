from django import forms
<<<<<<< HEAD
from django.forms import ModelForm, PasswordInput, RadioSelect, DateInput
from homepage.models import User, Account, Transaction, Goal

from material import *

class UserForm(ModelForm):
    class Meta:
        model = User
        # password = CharField(widget=forms.PasswordInput)
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        widgets = {
            'password': PasswordInput(),
        }

    layout = Layout(
         Row('first_name', 'last_name'),
         Row('username'),
         Row('email'),
         Row('password')
        )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    # def clean(self):
    #     user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
    #     if user == None:
    #         raise forms.ValidationError('Something went wrong.  Please try again.')
    #     return self.cleaned_data

account_types = (
                    ('CH', 'Checking'),
                    ('CC', 'Credit Card'),
                    ('in', 'Investments'),
                    ('LN', 'Loans'),
                    ('SV', 'Savings'),
                )
class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ('account_name', 'acc_type', 'acc_username', 'acc_password')
        widgets = {
            'acc_password': PasswordInput(),
        }
        labels = {
                    'acc_username':'Username',
                    'acc_password': 'Password',
                    'account_name': 'Institution name',
                    'acc_type': 'Type of account'
                 }

    layout = Layout(
                     Fieldset("Account Information",
                                Row('account_name', 'acc_type')
                             ),
                     Fieldset("Account Credentials",
                                Row('acc_username'),
                                Row('acc_password')
                             )
                    )

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('category','date','description','original_description','amount')
    layout = Layout(
                        Row('date', 'amount', 'category'),
                        Row('description'),
                        Row('original_description')
                   )

class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = ('goal_name', 'amount', 'goal_date')
        widgets = {
            'goal_date': DateInput(),
        }
        labels = {
                    'goal_name': 'Goal Name',
                    'amount': 'Amount',
                    'goal_date': 'Date'
        }
    layout = Layout(
                    Fieldset("Goal Information",
                            Row('goal_name'),
                            Row('amount', 'goal_date')
                        )
                    )
