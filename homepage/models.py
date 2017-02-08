from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Inherited from AbstractUser and AbstractBaseUser
    # password
    # last_login
    # first_name
    # last_name
    # email
    # is_staff
    # help_text
    # is_active
    # date_joined
    securtiy_question = models.TextField(max_length=150, null=True, blank=True)
    pass

class Account(models.Model):
    user = models.ForeignKey(User, null=True)
    account_name = models.CharField(max_length=75, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    account_types = (
                        ('CH', 'Checking'),
                        ('CC', 'Credit Card'),
                        ('IN', 'Investments'),
                        ('LN', 'Loans'),
                        ('SV', 'Savings'),
                    )
    acc_type = models.CharField(max_length=2, choices=account_types, default='CH')
    acc_username = models.CharField(max_length=45, null=False, blank=False)
    acc_password = models.CharField(max_length=45, null=False, blank=False)

    def __str__(self):
        return self.account_name

class Goal(models.Model):
    user = models.ForeignKey(User, null=True)
    goal_name = models.CharField(max_length=75, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    goal_date = models.DateField(null=True, blank=True)
    type_choices = (
                        ('Savings', 'Saving for'),
                        ('Budget', 'Budget item'),
                   )
    goal_type = models.CharField(max_length=7, choices=type_choices, default='Savings')
    description = models.TextField(max_length=255, null=True, blank=True)

class Transaction(models.Model):
    account = models.ForeignKey(Account, null=True)
    category_choices = (
                            ('rent', 'Rent'),
                            ('groceries', 'Groceries'),
                            ('gas', 'Gas'),
                            ('restaurant', 'Restaurant'),
                            ('entertainment', 'Entertainment'),
                            ('movies', 'Movies'),
                            ('utilities', 'Utilities'),
                            ('insurance', 'Insurance'),
                            ('electronics', 'Electronics'),
                            ('shopping', 'Shopping'),
                            ('misc', 'Misc.'),
                       )
    category = models.CharField(max_length=20, choices=category_choices, default='misc')
    date = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=75, null=True, blank=True)
    original_description = models.TextField(max_length=75, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
