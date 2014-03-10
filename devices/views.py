from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django import forms

# Create your views here.
from devices.models import Device
from facilities.models import Facility


class AddDeviceToFacilityForm(forms.Form):
    devices = forms.ModelChoiceField(queryset=Device.objects.all())


class RemoveDeviceForm(forms.Form):
    devices = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(RemoveDeviceForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['devices'].queryset = user.facilities.all()[:1].get().devices.all()

@login_required
def index(request):
    context = {}
    return render(request, 'devices/index.html', context)

@login_required
@permission_required('devices.add_device')
def add(request):
    if request.method == 'POST':
        form = AddDeviceToFacilityForm(request.POST)
        if form.is_valid():
            devices = form.cleaned_data['devices']
            facility = Facility.objects.get(pk=request.user.facilities.all()[:1].get().id)
            facility.devices.add(devices)

    all_devices = Device.objects.all()
    user_devices = request.user.facilities.all()

    form = AddDeviceToFacilityForm

    context = {'devices': all_devices, 'facilities': user_devices, 'form': form}
    return render(request, 'devices/add.html', context)


def view(request):
    user_facilities = Facility.objects.get(pk=request.user.facilities.all()[:1].get().id)
    user_facilities_devices = user_facilities.devices.all()
    return render(request, 'devices/view.html', {'devices': user_facilities_devices})

@login_required()
def remove_device(request):
    if request.method == 'POST':
        form = RemoveDeviceForm(request.POST, user=request.user)
        if form.is_valid():
            device = form.cleaned_data['devices']
            request.user.facilities.all()[:1].get().devices.remove(device)
            messages.success(request, 'Device removed.')
            return render(request, "index.html")

    context = {
        'form': RemoveDeviceForm(user=request.user)
    }
    return render(request, 'devices/remove_device.html', context)