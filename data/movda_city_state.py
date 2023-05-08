import json

with open("location_data.json", "r", encoding="utf-8") as file:
    movida_location = json.loads(file.read())

with open("estados-cidades.json", "r", encoding="utf-8") as file:
    brazil_location = json.loads(file.read())

brazilian_states = brazil_location["states"]
brazilian_cities = brazil_location["cities"]


def delete_equals(dic, condition):
    l = []
    for i in dic:
        if condition.upper() not in i:
            l.append(i)

    return l


dic_brazilian_cities = {}
j = 0
dic = {}
for i in brazil_location["cities"]:
    dic[j] = i["name"]





"""
movida_json_list = list(movida_location.keys())
airport = delete_equals(sorted(movida_location.keys()), "aeroporto")
shopping = delete_equals(airport, "shopping")
hifen = delete_equals(shopping, "-")
"""

