import datetime
from django import forms
from django.db.models import Avg
from django.http import Http404, HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from devices.models import Device
from measurements.models import Measurement, Time
from measurements.serializers import MeasurementSerializer


class AddMeasurementToDeviceForm(forms.Form):

    times = forms.ModelChoiceField(queryset=Time.objects.all())
    user_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super(AddMeasurementToDeviceForm, self).__init__(*args, **kwargs)
        if user_id:
            self.fields['user_id'].initial = user_id


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


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
    form = AddMeasurementToDeviceForm(user_id=1)
    return render(request, 'measurements/add.html', {'form': form})


def measurements_list(request):
    measurements = Measurement.objects.all()
    serializer = MeasurementSerializer(measurements)
    return JSONResponse(serializer.data)


class MeasurementViewSet(viewsets.ViewSet):
    model = Measurement

    def list(self, request):
        device_model = request.GET.get('device_model')

        if not device_model:
            return JSONResponse({})

        device = Device.objects.get(model__contains=device_model)

        measurements = device.measurement_set.values('time').annotate(value=Avg('value'))

        return JSONResponse(measurements)