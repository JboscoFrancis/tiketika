from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.db import IntegrityError
from django.contrib.auth import login, logout
from django.contrib import messages


def registration(request):
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirm-password']

        if password!=confirmpassword:
            messages.warning(request, f"password don't match")
        else:
            #create user
            try:
                user = User.objects.create_user(
                    username,
                    email,
                    password
                )
                login(request,user)
                messages.success(request, f'account for ' + username + ' created successfully')
                return redirect('home')
            except IntegrityError:
                messages.warning(request, f'username already exist')
                return redirect('register')
    return render(request, 'users/register.html')

def agent_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'you have log in successfully')
            return redirect('home')
        else:
            messages.warning(request, f'invalid username or password')
    return render(request, 'users/login.html')

def agent_logout(request):
    logout(request)
    return redirect('home')