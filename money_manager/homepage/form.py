from django.forms import ModelForm
from django import forms
from .models import UserDetails, Transactions

class TransactionForm(ModelForm):
    class Meta:
        model = Transactions
        # fields = ['transaction_amount']
        fields = ['transaction_amount', 'purpose']

class Profile(ModelForm):
    class Meta:
        model = UserDetails
        fields = ['name', 'age', 'occupation', 'salary']

class FilterForm(forms.Form):
    start_year = forms.IntegerField()
    start_month =forms.IntegerField()
    start_day =forms.IntegerField()
    end_year =forms.IntegerField()
    end_month =forms.IntegerField()
    end_day =forms.IntegerField()


        