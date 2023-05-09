import json


class Information:
    def __init__(self, city):
        self.city = city

    # This function is responsible to search all information about the city informed by user, like the city code,
    # city id, city latitude, city longitude and if the movida store in that location works 24 hours per day or no.
    def search_possible_location_json(self):
        with open("../data/location_data.json", "r", encoding="utf-8") as file:
            file = json.load(file)

        try:
            return file[self.city.upper()]
        except():
            print("Location not found. Please try with the right location")


