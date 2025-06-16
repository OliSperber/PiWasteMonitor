import geocoder

class GeoCoder:
    def get_coords():
        g = geocoder.ip('me')
        if g.ok and g.latlng:
            return g.latlng[0], g.latlng[1]
        else:
            print("Kon locatie via IP niet bepalen.")
            return 0.0, 0.0