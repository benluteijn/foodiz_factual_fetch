# Factual API hack to fetch restaurant data

## Description of project

As part of my startup Foodiz (rating dishes instead of restaurants), I needed to get the list of all the restaurants within the cities I was targeting (Manhattan, Brooklyn and Paris). I got a partial dataset thanks to a contract signed with SinglePlatform, but I quickly realized it wasn't complete. I had to look for other datasources, and found a provider named Factual. Going through my discussions with them, they wanted to bill me $1000 / month for at least 12 month in order to get the "large data extract" from their databases for Paris and NYC. 

Instead, I decided to exploit a weakness in their API to get the extract for free. All the code is written in Python, and the data was later consumed in a Node.js application database (javascript based)

## Files description
- step 1 - factual connector: probably the most interesting piece of code. It describes how the API hack works, and how a city is dynamically reduced to a set of smaller and smaller sub-rectangles until an API call yields a number of results that fall below the API limit of 500 results. 
- step 1b - filter json extract: data cleansing
- step 2 - remove factual in common: prepare data from my current database and Factual, by removing the already existing Factual locations within my database
- step 3 - remove heuristically locations: remove locations from my database that may already have a match within the factual extract based on a heuristic. The heuristic has components based on geographic proximity and restaurant name fuzzy matching. A lot of tuning was done in this step to ensure the matchs were optimal
- step 4 - data conversion process so it could be ingested within my database and data model

## Visualization
As a QA process, and to make sure I had captured most of the restaurants within a city, I plotted them on a blank canvas based on captured lat/lon. For Paris, the restaurants clearly outlined every major (and minor) streets. It's a cool representation of Paris and its streets, only by showing a dot at every restaurant location

## References

Factual API: http://developer.factual.com/
SinglePlatform: http://www.singleplatform.com/




