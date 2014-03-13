from xml.etree import ElementTree
from django.http import HttpResponse
import requests

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from flickr_images.models import FlickrImage


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class ImagesViewSet(viewsets.ViewSet):
    model = FlickrImage

    def list(self, request):

        # Search for images by tag on the Flickr REST API
        response = requests.get('https://api.flickr.com/services/rest/', params={
            'tags': 'solar',
            'per_page': '1',

            # Mandatory parameters
            'method': 'flickr.photos.search',
            'format': 'json',
            'api_key': '7a0a6d9d6aa08ea6360f33561aa56645',
            'nojsoncallback': '1'
        })

        if response.status_code == 200:
            return JSONResponse(response.json())

        return JSONResponse({})