from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register_page(request):
    if request.method == "POST":
        # return HttpResponse("Hello World")
        print(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # saves the user to the django user database
            messages.success(request, f'Successfully registered!')
            return redirect('login')
        else:
            return render(request, "login/login.html")

    else:
        form = UserCreationForm()  
    return render(request, "login/register.html", {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f'{username}---{password}')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)    # Attaches a session to the user
            return redirect(f'/homepage/{username}')
        
        else:
            return render(request, 'login/login.html')

    return render(request, "login/login.html")


def logout_user(request):
    logout(request)
    return redirect('/')