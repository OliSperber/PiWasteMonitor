from geopy.geocoders import Nominatim

class GeoCoder:
    def __init__(self, user_agent="piwastemonitor"):
        self.geolocator = Nominatim(user_agent=user_agent)

 def get_coords(self):
        g = geocoder.ip('me')
        if g.ok and g.latlng:
            return g.latlng[0], g.latlng[1]
        else:
            print("Kon locatie via IP niet bepalen.")
            return 0.0, 0.0