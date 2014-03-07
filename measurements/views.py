from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'measurements/index.html', context)