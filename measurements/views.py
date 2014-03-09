from django import forms
from django.shortcuts import render
from rest_framework import viewsets
from devices.models import Device
from measurements.models import Measurement, Time
from measurements.serializers import MeasurementSerializer
from django.contrib.auth.models import User


class AddMeasurementToDeviceForm(forms.Form):

    times = forms.ModelChoiceField(queryset=Time.objects.all())
    user_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super(AddMeasurementToDeviceForm, self).__init__(*args, **kwargs)
        if user_id:
            self.fields['user_id'].initial = user_id


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
    form = AddMeasurementToDeviceForm(user_id=1)
    return render(request, 'measurements/add.html', {'form': form})


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer