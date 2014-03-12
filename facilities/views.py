from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.db import connection
from django.shortcuts import render
from django.forms import ModelForm
from facilities.models import Facility
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User, Group


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


class RegisterResidentForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()


class DeleteResidentForm(forms.Form):
    users = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DeleteResidentForm, self).__init__(*args, **kwargs)
        if user:
            user_facilities = user.facilities.all()[:1].get()
            self.fields['users'].queryset = Facility.objects.get(pk=user_facilities.id).users.all().exclude(pk=user.id)


def index(request):
    context = {}
    return render(request, 'facilities/index.html', context)


@login_required
@permission_required('facilities.add_facility')
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
            group = Group.objects.get(name="facility_owners")
            group.user_set.add(user)
            user.save()
            messages.success(request, 'Your account has been created.')
            return render(request, 'index.html')

    context = {
        'form': RegisterForm
    }
    return render(request, 'facilities/register.html', context)


@login_required
@permission_required('facilities.add_resident')
def register_resident(request):
    if request.method == 'POST':
        form = RegisterResidentForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            group = Group.objects.get(name="facility_residents")
            group.user_set.add(user)
            user.facilities.add(request.user.facilities.all()[:1].get())
            user.save()
            messages.success(request, 'Resident created.')
            return render(request, 'index.html')

    facility_id = request.user.facilities.all()[:1].get().id

    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(facility_id) FROM facilities_facility_users WHERE facility_id=%s", [facility_id])

    amount_of_residents = cursor.fetchone()
    amount_of_residents = amount_of_residents[0]

    context = {
        'amount_of_residents': amount_of_residents
    }

    if amount_of_residents < 5:
        context = {
            'form': RegisterResidentForm,
            'amount_of_residents': amount_of_residents
        }

    return render(request, 'facilities/register_resident.html', context)


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return render(request, 'index.html')


@login_required
def delete_resident(request):
    if request.method == 'POST':
        form = DeleteResidentForm(request.POST, request.user)
        if form.is_valid():
            user = form.cleaned_data['users']
            user.delete()
            messages.success(request, 'User deleted.')
            return render(request, 'index.html')

    context = {
        'form': DeleteResidentForm(user=request.user)
    }
    return render(request, 'facilities/delete_resident.html', context)


def process_oauth2_login(request):
    group = Group.objects.get(name="facility_owners")
    group.user_set.add(request.user)
    return render(request, 'index.html')