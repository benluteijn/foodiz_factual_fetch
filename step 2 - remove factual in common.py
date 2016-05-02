import csv
import ijson

__author__ = 'steph'


# need to download all the restaurants city = "New York" from the database - gives a json file

# to hedge for error: Decimal('40.75509') is not JSON serializable
import simplejson as json
from pprint import pprint

with open('Location - filtered New York.json') as data_file:
    data = json.load(data_file)

# loop over all the existing factual keys and store them in a dict for O(1) access
existingFactualKeys = {}
for parseLocation in data["results"]:
    if parseLocation["source"]=="factual":
        existingFactualKeys[parseLocation["location_id"]]=0


def cleanText(text):
    return text.replace(',','').replace("\t",'').replace("\n",'').encode('ascii', 'ignore')


def extractInfoFromFactualJSON(factualJSON):
    address =  cleanText(factualJSON.get("address",""))
    tel = cleanText(factualJSON.get("tel",""))
    name = cleanText(factualJSON.get("name",""))
    locality = cleanText(factualJSON.get("locality",""))
    country = cleanText(factualJSON.get("country",""))
    latitude = factualJSON.get("latitude","")
    longitude = factualJSON.get("longitude","")
    postcode = cleanText(factualJSON.get("postcode",""))
    factual_id = cleanText(factualJSON.get("factual_id",""))
    return [address, tel, name, locality, country, latitude, longitude, postcode, factual_id]


i = 0
finalData = []
with open('resultsForBrooklyn.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    finalData = [reader.fieldnames]
    for line in reader:
        if not (line["factual_id"]) in existingFactualKeys:
            finalData.append(extractInfoFromFactualJSON(line))

with open('resultsForBrooklyn - after step 2.csv', 'wb') as f:
    a = csv.writer(f, delimiter=',')
    a.writerows(finalData)


# print(i)
