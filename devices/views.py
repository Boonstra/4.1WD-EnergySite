from django.shortcuts import render
from django import forms

# Create your views here.
from devices.models import Device
from facilities.models import Facility


class AddDeviceToFacilityForm(forms.Form):
    devices = forms.ModelChoiceField(queryset=Device.objects.all())


def index(request):
    context = {}
    return render(request, 'devices/index.html', context)


def add(request):
    if request.method == 'POST':
        form = AddDeviceToFacilityForm(request.POST)
        if form.is_valid():
            devices = form.cleaned_data['devices']
            facility = Facility.objects.get(pk=request.user.facilities.all()[:1].get().id)
            facility.device_set.add(devices)

    all_devices = Device.objects.all()
    user_devices = request.user.facilities.all()

    form = AddDeviceToFacilityForm

    context = {'devices': all_devices, 'facilities': user_devices, 'form': form}
    return render(request, 'devices/add.html', context)


def view(request):
    user_facilities = request.user.facilities.all()
    user_facilities_devices = user_facilities.devices.all()
    return render(request, 'view.html', {'devices': user_facilities_devices})