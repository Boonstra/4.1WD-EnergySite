from django.contrib import messages
from django.shortcuts import render
from django.forms import ModelForm
from facilities.models import Facility
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.

class AddFacilityForm(ModelForm):
    class Meta:
        model = Facility
        fields = ['street', 'street2', 'city', 'zipcode', 'inhabitants', 'email', 'phone_number', 'password']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

def index(request):
    context = {}
    return render(request, 'facilities/index.html', context)

def add(request):
    if request.method == 'POST':
        form = AddFacilityForm(request.POST)
        if form.is_valid():
            form.save()

    form = AddFacilityForm()
    context = {
        'form': form
    }
    return render(request, 'facilities/add.html', context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    messages.success(request, 'You have been logged in successfully!')
                    return render(request, 'index.html')
                else:
                    messages.error(request, 'Your account is inactive.')
            else:
                messages.error(request, 'Your credentials did not match anything on record.')

    form = LoginForm
    context = {
        'form': form
    }
    return render(request, 'facilities/login.html', context)

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return render(request, 'index.html')