import ijson

__author__ = 'steph'


# need to download all the restaurants city = "New York" from the database - gives a json file

# to hedge for error: Decimal('40.75509') is not JSON serializable
import simplejson as json

counterNewYork = 0
counter = 0
finalArray = []
with open('Location.json') as data_file:
    for item in ijson.items(data_file, "results.item"):
        counter += 1
        if counter % 100 == 0:
            print (counter)
        if (item["city"]=="New York"):
            finalArray.append(item)
            counterNewYork += 1

print(counterNewYork)

results = {}
results["results"] = finalArray

with open('Location - filtered New York.json', 'w') as outfile:
    json.dump(results, outfile)