from django.shortcuts import render, redirect, HttpResponse
from .models import UserDetails, Transactions
from django.contrib.auth.models import User
from .form import TransactionForm, Profile, FilterForm
from django.contrib.auth.decorators import login_required
from datetime import datetime


@login_required(login_url="login/")
def homepage(request, pk):
    context = {}
    context['pk'] = pk
    user_id = User.objects.filter(username=pk).values()[0]
    user_details = UserDetails.objects.filter(user_id=user_id['id'])
    print(user_details)
    if len(user_details) == 0:
        print("Creating a new profile...........")
        return profile(request, pk, user_id)

    else:
        filter_form = FilterForm()
        context['user_data'] = user_details.all()[0]
        context['filter_form'] = filter_form
        if request.method == 'POST':
            filter_form=FilterForm(request.POST)
            print(filter_form['start_day'].value())
            start_year = int(filter_form['start_year'].value())
            start_month = int(filter_form['start_month'].value())
            start_day = int(filter_form['start_day'].value())
            end_year = int(filter_form['end_year'].value())
            end_month = int(filter_form['end_month'].value())
            end_day = int(filter_form['end_day'].value())
            print(start_day, end_day)
            start_date = datetime(year=start_year, month=start_month, day=start_day, hour=0, minute=0)
            end_date = datetime(year=end_year, month=end_month, day=end_day, hour=0, minute=0)
            transactions = Transactions.objects.filter(user_id=user_id['id']).order_by('-created').filter(created__date__range=[start_date, end_date])#ordered by latest time
            # transactions = Transactions.objects.filter(user_id=user_id['id']).order_by('-created').filter(created__time__range=[start_date, end_date])#ordered by latest time
        else:
            transactions = Transactions.objects.filter(user_id=user_id['id']).order_by('-created')
        
        if len(transactions) != 0:
            context['transactions'] = transactions
        else:
            context['transactions'] = None

    return render(request, 'homepage/homepage.html', context)


@login_required(login_url="login/")
def transaction(request, pk):
    form = TransactionForm()
    if request.method == 'POST':
        user = User.objects.filter(username=pk).all()[0]
        transaction_amount = request.POST.get('transaction_amount')
        purpose = request.POST.get('purpose')
        transaction = Transactions(user_id=user, transaction_amount=transaction_amount, purpose=purpose)
        transaction.save()
        return homepage(request, pk)
    else:
        return render(request, f'homepage/transaction.html', {'form':form})


@login_required(login_url="login/")
def profile(request, pk, user_id):
    profile_form = Profile(request.POST)
    if request.method == 'POST':
        new_user = UserDetails(name=request.POST['name'], age=request.POST['age'], occupation=request.POST['occupation'], salary=request.POST['salary'], user_id=user_id['id'])
        new_user.save()
        return homepage(request, pk)

    else:
        return render(request, 'homepage/profile.html', {'form': profile_form})
