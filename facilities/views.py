from django.shortcuts import render
from django.forms import ModelForm
from facilities.models import Facility

# Create your views here.

class AddFacilityForm(ModelForm):
    class Meta:
        model = Facility
        fields = ['street', 'street2', 'city', 'zipcode', 'inhabitants', 'email', 'phone_number', 'password']

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