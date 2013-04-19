import geopy

from django.contrib.gis.geos import fromstr


def geocode(obj):
        """
        Returns location [STRING], latlng [TUPLE]
        
        """
        
        city = obj.city
        state = obj.state
        address1 = obj.address1
        geocoder = geopy.geocoders.googlev3.GoogleV3()
        loc, latlng = None, None
        try:
            loc, latlng = geocoder.geocode("%s, %s, %s" %(address1, city, state))
        except:
            
            msg = "[%s ID %s]Geocoder failed for location: %s, %s, %s" %(obj, obj.id, address1, city, state)
            print msg
            
            
        return loc, latlng     
         
    
def update_geocode(obj, fieldname='geolocation'):
        """
        Uses self.geocode() to geocode itself and then if a valid
        latlng is returned, saves to database.

        :param feildname: [String] The fieldname on the object to save the point object to.
                                    If this is a model, it should be a PointField

        :return location: [STRING]

        :return latlng: [TUPLE] 

        """
        location, latlng = geocode(obj)
        if latlng:
            pnt = fromstr( 'POINT(%s %s)' %(latlng[1],latlng[0]) )    
            obj.__setattr__(fieldname, pnt)
            obj.save()
        return location, latlng

def geocode_zipcode(zipcode):
    geocoder = geopy.geocoders.googlev3.GoogleV3()
    try:
        loc, latlng = geocoder.geocode(zipcode)
    except:
        loc = None
        latlng = []
        msg = "Geocoder failed for location: %s" %(zipcode)
        print msg
            
            
    return loc, latlng     