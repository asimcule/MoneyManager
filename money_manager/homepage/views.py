from django.shortcuts import render, redirect, HttpResponse
from .models import UserDetails, Transactions
from django.contrib.auth.models import User
from .form import TransactionForm, Profile, FilterForm
from django.contrib.auth.decorators import login_required
from datetime import datetime


@login_required(login_url="/")
def homepage(request):
    context = {}
    context['pk'] = request.user
    user_id = User.objects.filter(username=request.user).values()[0]
    user_details = UserDetails.objects.filter(user_id=user_id['id'])
    print(user_details)
    if len(user_details) == 0:
        print("Creating a new profile...........")
        return profile(request, request.user, user_id)
    else:
        context['user_data'] = user_details.all()[0]
        if request.method == 'POST':
            # Filtering
            print('inside the post block')
            start_year = int(request.POST['start_year'])
            start_month = int(request.POST['start_month'])
            start_day = int(request.POST['start_day'])
            end_year = int(request.POST['end_year'])
            end_month = int(request.POST['end_month'])
            end_day = int(request.POST['end_day'])
            print(start_day, end_day)
            start_date = datetime(year=start_year, month=start_month, day=start_day, hour=0, minute=0)
            end_date = datetime(year=end_year, month=end_month, day=end_day, hour=0, minute=0)
            transactions = Transactions.objects.filter(user_id=user_id['id']).order_by('-created').filter(created__date__range=[start_date, end_date])#ordered by latest time
            print(transactions)
        else:
            # No filtering
            print('inside the default block')
            transactions = Transactions.objects.filter(user_id=user_id['id']).order_by('-created')
        
        # Validation
        if len(transactions) != 0:
            context['transactions'] = transactions
        else:
            context['transactions'] = None

    return render(request, 'homepage/homepage.html', context)



@login_required(login_url="/")
def transaction(request):
    form = TransactionForm()
    if request.method == 'POST':
        user = User.objects.filter(username=request.user).all()[0]
        transaction_amount = request.POST.get('transaction_amount')
        purpose = request.POST.get('purpose')
        transaction = Transactions(user_id=user, transaction_amount=transaction_amount, purpose=purpose)
        transaction.save()
        return redirect('homepage')
    else:
        return render(request, f'homepage/transaction.html', {'form':form})



@login_required(login_url="/")
def profile(request, pk, user_id):
    profile_form = Profile(request.POST)
    if request.method == 'POST':
        new_user = UserDetails(name=request.POST['name'], age=request.POST['age'], occupation=request.POST['occupation'], salary=request.POST['salary'], user_id=user_id['id'])
        new_user.save()
        return redirect('homepage')

    else:
        return render(request, 'homepage/profile.html', {'form': profile_form})
