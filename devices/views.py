from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

def index(request):
    context = {}
    return render(request, 'devices/index.html', context)

def add(request):
    user = authenticate(username='Erik', password='hahaha123')
    if user is not None:
        if user.is_active:
            print("User is valid, active and authenticated")
        else:
            print("The password is valid, but the account has been disabled!")
    else:
        print("The username and password were incorrect")

    context = {}
    return render(request, 'devices/add.html', context)