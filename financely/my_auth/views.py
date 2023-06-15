from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


def create_acc_view(request):
    return render(request, 'my_auth/signup')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('/dashboard/')
        else:
            # Return an 'invalid login' error message.
            context = {"error": "Invalid username or password"}
            return render(request, 'my_auth/login.html', context)
    return render(request, 'my_auth/login.html')

def logout_view(request):
    logout(request)
    return login_view(request)

def home_view(request):
    return render(request, 'base.html')
