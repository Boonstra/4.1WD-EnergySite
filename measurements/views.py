from django import forms
from django.shortcuts import render
from devices.models import Device
from measurements.models import Measurement, Time
from django.contrib.auth.models import User


class AddMeasurementToDeviceForm(forms.Form):
    times = forms.ModelChoiceField(queryset=Time.objects.all())


def index(request):
    # TODO Get current facility ID
    # Get all measurements
    measurements = Measurement.objects.filter(facility_id=1).order_by('device__id', 'time__time')

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
    form = AddMeasurementToDeviceForm()
    return render(request, 'measurements/add.html', {'form': form})