import csv
from pprint import pprint
import unicodedata
import re
import json
import simplejson

regex = r"[a-z]+"


def strip_accents(s):
    encoding = "utf-8" # or iso-8859-15, or cp1252, or whatever encoding you use
    unicode_string = s.decode(encoding)
    return ''.join(c for c in unicodedata.normalize('NFD', unicode_string)
                   if unicodedata.category(c) != 'Mn')


def keywords_from_string(s):
    return re.findall(regex, strip_accents(s).lower())


def parseJSONForLocation(location):
    result = {}
    result["address1"] = location["address"]
    result["address1_lc"] = location["address"].lower()
    result["address1_keywords"] = keywords_from_string(location["address"])
    result["businessType"] = "Restaurant"
    result["city"] = location["locality"]
    result["city_lc"] = location["locality"].lower()
    result["city_keywords"] = ["new", "york"]
    result["country"] = "US"
    result["currency"] = "USD"
    result["error_bool"] = False
    result["geo"] = {"__type": "GeoPoint", "latitude": float(location["latitude"]), "longitude": float(location["longitude"])}
    result["latitude"] = float(location["latitude"])
    result["location_id"] = location["factual_id"]
    result["longitude"] = float(location["longitude"])
    result["menus"] = []
    result["n_items"] = 0
    result["n_menus"] = 0
    result["name"] = location["name"]
    result["name_lc"] = location["name"].lower()
    result["name_keywords"] = keywords_from_string(location["name"])
    result["outOfBusiness"] = "f"
    result["phone"] = location["tel"]
    result["postcode"] = location["postcode"]
    result["region"] = "NY"
    result["source"] = "factual"
    result["status"] = "completed"
    return result


with open('resultsForBrooklyn - after step 3.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    finalData = []
    for location in reader:
        finalData.append(parseJSONForLocation(location))
    data = { "results" : finalData}
    smalldata = { "results" : [finalData[0]]}


with open('data import - step 4.json', 'w') as outfile:
    outfile.write(simplejson.dumps(data , indent=4, sort_keys=True))


with open('data import - sample.json', 'w') as outfile:
    outfile.write(simplejson.dumps(smalldata , indent=4, sort_keys=True))