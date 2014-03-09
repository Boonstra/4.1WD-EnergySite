from django.contrib import messages
from django.shortcuts import render
from django.forms import ModelForm
from facilities.models import Facility
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User


# Create your views here.

class AddFacilityForm(ModelForm):
    class Meta:
        model = Facility
        fields = ['street', 'street2', 'city', 'zipcode', 'inhabitants', 'email', 'phone_number', 'password']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()


def index(request):
    context = {}
    return render(request, 'facilities/index.html', context)

def add(request):
    if request.method == 'POST':
        form = AddFacilityForm(request.POST)
        if form.is_valid():
            street = form.cleaned_data['street']
            street2 = form.cleaned_data['street2']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            inhabitants = form.cleaned_data['inhabitants']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            form.save()
            test = Facility.objects.get(street=street, street2=street2, city=city, zipcode=zipcode, inhabitants=inhabitants, email=email, phone_number=phone_number, password=password)
            user = request.user
            user.facilities.add(test)

    form = AddFacilityForm()
    context = {
        'form': form
    }
    return render(request, 'facilities/add.html', context)

def view(request):
    user_facilities = request.user.facilities.all()
    return render(request, 'facilities/view.html', {'facilities': user_facilities})

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

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, 'Your account has been created.')
            return render(request, 'index.html')

    form = RegisterForm
    context = {
        'form': form
    }
    return render(request, 'facilities/register.html', context)

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return render(request, 'index.html')