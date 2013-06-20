import json

from django.conf import settings
from django.forms import Widget
from django.template.loader import render_to_string


class GeomWidget(Widget):
    """
    An interactive map widgets that outputs a GeoJSON object
    to a textarea. 

    """
   
    template_name = "fieldsites/widgets/geom_widget.html"

    def render(self, name, value, attrs=None):
        
        if value == "{}": value = ""
                

        if value:
          if not value.__class__ == u''.__class__:
            value = json.dumps(value)


        tv = {'value':value,
              'name':name,
              'INITIAL_LAT':settings.INITIAL_LAT,
              'INITIAL_LON':settings.INITIAL_LON,
              'INITIAL_ZOOM':settings.INITIAL_ZOOM,
              'CLOUDMADE_API_KEY':settings.CLOUDMADE_API_KEY, 
             }
        
        html = render_to_string(self.template_name, tv)
        return html