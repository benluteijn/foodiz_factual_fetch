import csv
import json
from fuzzywuzzy import fuzz

__author__ = 'steph'

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


with open('Location - filtered New York.json') as data_file:
# with open('Location - New York extract.json') as data_file:
    data = json.load(data_file)
    listOfNewYorkLocations = data["results"]

# retrieve all the singleplatform locations to be matched
singlePlatformLocations = []
for parseLocation in listOfNewYorkLocations:
    if parseLocation["source"]=="singleplatform":
        singlePlatformLocations.append(parseLocation)


i = 0


def extractInfoFromFactualJSON(factualJSON):
    address =  factualJSON.get("address","")
    tel = factualJSON.get("tel","")
    name = factualJSON.get("name","")
    locality = factualJSON.get("locality","")
    country = factualJSON.get("country","")
    latitude = factualJSON.get("latitude","")
    longitude = factualJSON.get("longitude","")
    postcode = factualJSON.get("postcode","")
    factual_id = factualJSON.get("factual_id","")
    return [address, tel, name, locality, country, latitude, longitude, postcode, factual_id]



with open('resultsForBrooklyn - after step 2.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    data = []
    dataMatched = []
    data.append(reader.fieldnames)
    dataMatched.append(reader.fieldnames)
    for candidateFactual in reader:
        i += 1
        lat1, lon1 = float(candidateFactual["latitude"]), float(candidateFactual["longitude"])
        nameFactual = candidateFactual["name"].strip().lower().replace('restaurant', '')
        if i % 100 == 0:
            print (i)
        matchFound = False
        for parseLocation in singlePlatformLocations:
            lat2, lon2 = parseLocation.get("latitude",0), parseLocation.get("longitude",0)
            nameParse = parseLocation["name"].strip().lower().replace('restaurant', '')
            if (haversine(lon1, lat1, lon2, lat2) <= 0.3 and
                    (nameFactual in nameParse or nameParse in nameFactual or fuzz.token_set_ratio(nameFactual,nameParse) >= 80 or fuzz.partial_ratio(nameFactual,nameParse) >= 80)):
                print(nameFactual, nameParse)
                matchFound = True
                break
        if not matchFound:
            data.append(extractInfoFromFactualJSON(candidateFactual))
        if matchFound:
            dataMatched.append(extractInfoFromFactualJSON(candidateFactual))

# write final results
with open('resultsForBrooklyn - after step 3.csv', 'wb') as f:
    a = csv.writer(f, delimiter=',')
    a.writerows(data)

# write matches
with open('dataMatched - after step 3.csv', 'wb') as f:
    a = csv.writer(f, delimiter=',')
    a.writerows(dataMatched)

