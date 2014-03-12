from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from images.models import Image


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class ImagesViewSet(viewsets.ViewSet):
    model = Image

    # TODO Implement
    def list(self, request):
        tags = 'tagsfromweek4'

        # Set up connection

        # Test data
        return JSONResponse([{'image'}, {'image'}])