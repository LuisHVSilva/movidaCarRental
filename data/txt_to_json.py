import json


# This function just open the file where the crude txt is.
def open_file(text_file):
    with open(text_file, "r", encoding="utf-8") as file:
        return file.read()


# This method transform the format provided by txt into json format
# Txt format -> { "value1" }, { "value2" }, ...
# Json format -> { "key1": { "value1" }, "key2": { "value2" }, ... }
def txt_to_json(text_file):
    txt = open_file(text_file).split("{\n")  # Breaking origin txt into some lists from breaks lines
    del txt[0]  # Deleting the first list index, it is a blank space

    l, i = [], 0  # declaring initial variables

    for t in txt:
        if t == 0:  # First string in text is the open json __value ({)
            l.append('{\n')
        else:  # The other strings is the part of json
            l.append('"' + str(i) + '":{\n' + t)

        i += 1

    txt = ""  # Creating full json text ("key": "__value")

    for t in l:
        txt = txt + "\n" + str(t)  # Putting key based in growing numbers
        txt = txt

    txt = json.loads("{\n" + txt + "\n}")  # Open and closing json
    return key_json_adjustment(txt)


# This method just change de primary numbers key of location dictionary and put the name of each location
def key_json_adjustment(txt):
    dic = {}
    for k, v in txt.items():
        dic[v["value"]] = txt[k]

    return dic


# This function write the JSON file with the information of crude_location_data.txt
def write_file(j, jf):
    json_object = json.dumps(j, indent=2)
    with open(jf, "w") as outfile:
        outfile.write(json_object)


txt_file = "../data/crude_location_data.txt"
json_file = "location_data.json"

json_format = txt_to_json(txt_file)
write_file(json_format, json_file)
