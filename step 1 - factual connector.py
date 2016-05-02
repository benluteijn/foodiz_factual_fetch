import json
from factual import Factual
from factual.utils import circle
import csv

factual = Factual('YOUR_KEY', 'YOUR_SECRET')
places = factual.table('places-us')

def getQueryForBoundaries(top,left,bottom,right):

    query = (places
             # .search('meatball shop')
             .filters(
                {
                    '$and': [
                        {
                            # restaurants and bars
                            'category_ids': {
                                '$includes_any': [
                                    312,
                                    347
                                ]
                            }
                        },
                        {
                            # new york and brooklyn
                            '$or': [
                                {
                                    'locality': {
                                        '$eq': 'new york'
                                    }
                                },
                                {
                                    'locality': {
                                        '$eq': 'brooklyn'
                                    }
                                }
                            ]
                        }
                    ]
                }
             )
             # [top,left],[bottom,right]
             # [34.06110,-118.42283],[34.05771,-118.41399]
             .geo({"$within": {"$rect": [[top, left], [bottom, right]]}})
             .limit(50)
             .include_count(True))
    return query

# brooklyn boundaries
top0 = 40.741429
left0 = -74.066190
bottom0 = 40.572916
right0 = -73.836508

def divideInFour(top,left,bottom,right):
    middleHorizontal = round((top + bottom)/2, 6)
    middleVertical = round((left + right)/2, 6)

    results = []
    results.append((top,left, middleHorizontal, middleVertical))
    results.append((top, middleVertical, middleHorizontal, right))
    results.append((middleHorizontal ,left, bottom, middleVertical))
    results.append((middleHorizontal, middleVertical, bottom, right))
    return results


def getAllResultsForQuery(query , total_row_count):
    default_limit = 50
    numIterPages = int((total_row_count - 1) / default_limit) + 1
    result = []
    for i in range(1, numIterPages+1):
        currentQuery = query.page(i, default_limit)
        result += currentQuery.data()
    return result


allSearches = [(top0,left0,bottom0,right0)]

i = 0
totalRestaurantCount = 0

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



with open('resultsForBrooklyn.csv', 'wb') as f:
    a = csv.writer(f, delimiter=',')
    a.writerows([["address","tel","name","locality","country","latitude","longitude","postcode","factual_id"]])
    while(len(allSearches)>0):
        i += 1
        print(i)
        currentBoundaries = allSearches.pop(0)
        query = getQueryForBoundaries(*currentBoundaries)
        total_row_count = query.total_row_count()
        if (total_row_count > 500):
            newBoundaries = divideInFour(*currentBoundaries)
            allSearches += newBoundaries
        else:
            totalRestaurantCount += total_row_count
            data = []
            for result in getAllResultsForQuery(query, total_row_count):
                data += [extractInfoFromFactualJSON(result)]
            a.writerows(data)

print(totalRestaurantCount)

#need to manually remove the duplicates afterwords (I had 9)
