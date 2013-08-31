import json
from copy import copy

from django.http import HttpResponse

from tastypie.resources import ModelResource
from tastypie.api import Api
from tastypie.utils.mime import determine_format, build_content_type


class ArcModelResource(ModelResource):
    """
    Returns the given resource as JSON.
    Use for calling the API in a view.

    Use this in place of tastypie.resources.ModelResource to add extra functionality.
    
    """
    def get_dict(self, request, order_by=None):
         # Get Active Cards from the tastypie API

        tmpRequest = copy(request)
        tmpRequest.GET = tmpRequest.GET.copy()
        tmpRequest.GET['format'] = 'json'
        if order_by: tmpRequest.GET['order_by'] = order_by

        outJSON = self.get_list(tmpRequest).content
        out = json.loads(outJSON)["objects"]

        return out, outJSON

class ArcApi(Api):
    

    def top_level(self, request, api_name=None):
        """
        A view that returns a serialized list of all resources registers
        to the ``Api``. Useful for discovery.
        
        Override this to add in docstrings to the top_level list of endpionts. 

        """
        available_resources = {}

        if api_name is None:
            api_name = self.api_name


        for name in sorted(self._registry.keys()):
            available_resources[name] = {
                'list_endpoint': self._build_reverse_url("api_dispatch_list", kwargs={
                    'api_name': api_name,
                    'resource_name': name,
                }),
                'schema': self._build_reverse_url("api_get_schema", kwargs={
                    'api_name': api_name,
                    'resource_name': name,
                }),
               'docstring':self._registry[name].__doc__
            }

        desired_format = determine_format(request, self.serializer)

        options = {}

        if 'text/javascript' in desired_format:
            callback = request.GET.get('callback', 'callback')

            if not is_valid_jsonp_callback_value(callback):
                raise BadRequest('JSONP callback name is invalid.')

            options['callback'] = callback

        serialized = self.serializer.serialize(available_resources, desired_format, options)
        return HttpResponse(content=serialized, content_type=build_content_type(desired_format))
