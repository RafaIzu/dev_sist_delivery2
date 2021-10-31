import requests
from geopy.distance import geodesic


class Geolocalization():
    def __init__(self):
        pass

    def calculate_distance(self, client_lat, client_lon):
        client_location = (client_lat, client_lon)
        shop_location = (-23.5710819, -46.649922)
        return round(geodesic(client_location, shop_location).km, 3)

    def __format_address_to_url(self, address, number, city, neighborhood,
                                state):
        return {"address": (number + "+" +address).replace(" ", "+"),
                "city": city.replace(" ", "+"),
                "neighborhood": neighborhood.replace(" ", "+"),
                "state": state.replace(" ", "+")}

    def gimmie_loc(self, address, number, city, neighborhood, state):
        formated_address = self.__format_address_to_url(address, number,
                                                        neighborhood, city,
                                                        state)
        formated_street = formated_address["address"]
        formated_city = formated_address["city"]
        formated_neighborhood = formated_address["neighborhood"]
        formated_state = formated_address["state"]
        request_https = "https://nominatim.openstreetmap.org/search?" +\
            f"street={formated_street}&"+\
            f"city={formated_city}" +\
            f"&county={formated_neighborhood}&" +\
            f"state={formated_state}&country=Brazil" +\
            f"&format=geocodejson"
        print("The URL for request is: ", request_https)
        response = requests.get(request_https)
        print(response.status_code)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            return response_json["features"][0]["geometry"]["coordinates"]
        else:
            return 404, 404
