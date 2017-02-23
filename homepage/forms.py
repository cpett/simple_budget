from django import forms
from django.forms import ModelForm, PasswordInput, RadioSelect, DateInput, ModelChoiceField, extras
from homepage.models import User, Account, Transaction, Goal
import urllib
import json

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
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    token = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
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
         Row('email'),
         Row('password')
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

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('account','category','date','description','original_description','amount')
        widgets = {
            'date': DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
    layout = Layout(
                        Row('account'),
                        Row('date', 'amount', 'category'),
                        Row('description'),
                        Row('original_description')
                   )
    def __init__(self, user, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        accounts = Account.objects.filter(user=user).values_list('account_name', flat=True)
        self.fields['account'].queryset = Account.objects.filter(account_name__in=accounts)

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
                    Row('goal_name'),
                    Row('goal_amount', 'goal_date'),
                    Row('goal_notes')
                    )
