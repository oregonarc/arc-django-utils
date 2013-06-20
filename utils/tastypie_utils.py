import json
from copy import copy
from tastypie.resources import ModelResource

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