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
        settings = FlickrImage.objects.all()[0]
        page = request.GET.get('page')
        per_page = request.GET.get('per_page')

        if not settings:
            return JSONResponse({})

        if not page:
            page = 1

        if not per_page:
            per_page = 1

        # Search for images by tag on the Flickr REST API
        search_response = requests.get('https://api.flickr.com/services/rest/', params={
            'tags': settings.tags,
            'page': page,
            'per_page': per_page,

            # Mandatory parameters
            'method': 'flickr.photos.search',
            'format': 'json',
            'api_key': '7a0a6d9d6aa08ea6360f33561aa56645',
            'nojsoncallback': '1',
        })

        if search_response.status_code != 200:
            return JSONResponse({})

        flickr_search_response = search_response.json()

        if flickr_search_response['stat'] != 'ok':
            return JSONResponse({})

        images = flickr_search_response['photos']['photo']

        detailed_images = []

        # Get information about the returned photos
        for image in images:
            detailed_response = requests.get('https://api.flickr.com/services/rest/', params={
                'photo_id': image['id'],
                'secret': image['secret'],

                # Mandatory parameters
                'method': 'flickr.photos.getInfo',
                'format': 'json',
                'api_key': '7a0a6d9d6aa08ea6360f33561aa56645',
                'nojsoncallback': '1',
            })

            if detailed_response.status_code != 200:
                continue

            flickr_detailed_response = detailed_response.json()

            if flickr_detailed_response['stat'] != 'ok':
                continue

            detailed_images.append(flickr_detailed_response['photo'])

        return JSONResponse({'images': detailed_images, 'refresh_rate': settings.refresh_rate})