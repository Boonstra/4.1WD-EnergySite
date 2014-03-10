import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets
from measurements.models import Measurement, Time
from devices.models import Device
from facilities.models import Facility
from measurements.serializers import MeasurementSerializer


class AddMeasurementToDeviceForm(forms.Form):
    times = forms.ModelChoiceField(queryset=Time.objects.all())
    devices = forms.ModelChoiceField(queryset=None)
    measurement = forms.FloatField(label='Measurement in kWh')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddMeasurementToDeviceForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['devices'].queryset = user.facilities.all()[:1].get().devices.all()


class ViewDeviceAveragesForm(forms.Form):
    device = forms.ModelChoiceField(queryset=Device.objects.all())


def index(request):
    try:
        facility_id = request.user.facilities.all()[0].id
    except:
        raise Http404

    # Get all measurements
    measurements = Measurement.objects\
        .filter(facility_id=facility_id, date__gte=datetime.date.today())\
        .order_by('device__id', 'time__time')

    # Put all measurements in a dictionary ordered by their device
    measurements_by_device = {}
    for measurement in measurements:
        if measurement.device not in measurements_by_device.keys():
            measurements_by_device[measurement.device] = {'measurements': [], 'totals': []}

        # Add measurement
        measurements_by_device[measurement.device]['measurements'].append(measurement)

        # Calculate/add totals
        if len(measurements_by_device[measurement.device]['totals']) > 0:
            previous_total = measurements_by_device[measurement.device]['totals'][-1]

            measurements_by_device[measurement.device]['totals'].append(measurement.value + previous_total)
        else:
            measurements_by_device[measurement.device]['totals'].append(measurement.value)

    # Get times
    times = Time.objects.all()

    context = {'measurements_by_device': measurements_by_device, 'times': times}

    return render(request, 'measurements/index.html', context)


def add(request):
    if request.method == 'POST':
        form = AddMeasurementToDeviceForm(request.POST, user=request.user)
        if form.is_valid():
            time = form.cleaned_data['times']
            device = form.cleaned_data['devices']
            measurement = form.cleaned_data['measurement']
            new_measurement = Measurement(date=datetime.date.today(), value=measurement)
            new_measurement.time_id = time.id
            new_measurement.device_id = device.id
            new_measurement.facility_id = request.user.facilities.all()[:1].get().id
            new_measurement.save()
            return render(request, 'measurements/index.html')

    form = AddMeasurementToDeviceForm(user=request.user)
    return render(request, 'measurements/add.html', {'form': form})


def view(request):
    if request.method == 'POST':
        form = ViewDeviceAveragesForm(request.POST)
        if form.is_valid():
            device = form.cleaned_data['device']
            measurements = Measurement.objects.filter(device_id=device.id)
            average = 0
            for measurement in measurements:
                average += measurement.value

            try:
                average = (average / measurements.count())
            except ZeroDivisionError:
                average = 0

            average = "{0:.2f}".format(average)
            context = {'average': average}
            return render(request, 'measurements/view.html', context)

    context = {'form': ViewDeviceAveragesForm}
    return render(request, 'measurements/view.html', context)


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer